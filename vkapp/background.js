var createdWindow;
var hidden = false;

function isHidden(){
	try {
		return createdWindow.outerBounds.height <= 30;
	} catch(e){
		return false;
	}
}

chrome.app.runtime.onLaunched.addListener(function() {
	chrome.app.window.create('vk.html',{
		id: 'vk',
		outerBounds:{
			height: 450,
			width: 300,
		},
		focused: true,
		alwaysOnTop: true,
		frame: 'none',
	}, function(cw){
		createdWindow = cw;
	});
});

function normalize(){


	console.log(createdWindow);


	chrome.system.display.getInfo(function(data){
		console.log(data);

		for (i in data){
			var display = data[i];

			if () {
				
			}
		}

	});

}

function show(){
	var inh = 450;

	createdWindow.outerBounds.height = 450;
	createdWindow.outerBounds.top -= inh - 30;
	
	normalize();
}

function hide(){
	var inh = createdWindow.outerBounds.height;

	createdWindow.outerBounds.height = 30;
	createdWindow.outerBounds.top += inh - 30;

	normalize();
}
function storage_set(key, value) {
	// Save it using the Chrome extension storage API.
	var dset = {};
	dset[key] = value;

	chrome.storage.local.set(dset, function() {
	});
}

function storage_get(key, callb) {
	chrome.storage.local.get(key, callb);
}

var VKTOKEN = '';

function vkLongPolling(){
	var self = this;

	var server = '';
	var ts = 0;
	var key = '';

	var first_time = true;


	self.ajax = function(url, method, data, callback) {
		var xhr = new XMLHttpRequest();
		xhr.open(method, url, true);
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				callback(JSON.parse(xhr.responseText));
			}
		}
		xhr.send();
	};

	self.vkMethod = function(method, data, callback){

		var datadef = {
			v: '5.60',
			access_token: VKTOKEN,
		}

		dataAll = {}

		for (i in datadef) {
			dataAll[i] = datadef[i];
		}
		for (i in data) {
			dataAll[i] = data[i];
		}

		var kv = [];

		for (i in dataAll){
			kv.push( i + "=" + encodeURIComponent(dataAll[i]));
		}

		var url = "https://api.vk.com/method/" + method + "?" + kv.join('&');

		self.ajax(url, 'GET', {}, callback)

	}
	self.init = function(){
		self.vkMethod("messages.getLongPollServer", {use_ssl: 0, need_pts: 0}, function(data){

			self.server = data.response.server;
			self.key = data.response.key;
			self.ts = data.response.ts;

			self.ask();
		});
	};
	self.ask = function(){
		var url = "https://" + self.server + "?act=a_check&key=" + self.key + "&ts=" + self.ts + "&wait=25&mode=10&version=1";

		self.ajax(url, 'GET', {}, function(data){

			self.ts = data.ts;

			self.ask();

			var runt = false;

			for(u in data.updates){
				if (data.updates[u][0] == 80) {
					runt = true;
				}
			}

			if (runt || self.first_time) {
				self.first_time = false;

				self.vkMethod('messages.getDialogs', {unread: 1}, function(data){
					var m = 0;


					for (i in data.response.items) {
						var mess = data.response.items[i];

						if (mess.message.push_settings) {

						} else {
							m++;
						}
					}
					
					chrome.runtime.sendMessage({
						action: "messages", 
						messages: m,
					}, function(response) {});

				});
			}

		});
	};

	self.init();

}

storage_get('vk_api', function(val,val1){
	if (val.vk_api) {
		VKTOKEN = val.vk_api;
		var vk = new vkLongPolling();
	} else {
		chrome.app.window.create('oauth.html',{
		});
	}
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "hide"){
		if (isHidden()){
			show();
		} else {
			hide();
		}
	}

	if (request.action == "titleclick"){
		if (isHidden()){
			show();
		}
	}
});