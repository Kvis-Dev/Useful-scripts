var createdWindow;
var hidden = false;
var WIN_MIN_HEIGHT = 40;

function isHidden(){
	try {
		return createdWindow.outerBounds.height <= WIN_MIN_HEIGHT;
	} catch(e){
		return false;
	}
}

function createWindow(){
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
		normalize();
		
		createdWindow.onClosed.addListener(function(){
			createdWindow = null;
		});

		createdWindow.onBoundsChanged.addListener(function() {
			normalize();
		});
		
	});
}
chrome.app.runtime.onLaunched.addListener(function() {
	createWindow();
});


function normalize(){
	if (!createdWindow) return;
	chrome.system.display.getInfo(function(data){
		for (i in data){
			var display = data[i];
			if (createdWindow.outerBounds.left > display.workArea.left && createdWindow.outerBounds.left < (display.workArea.left + display.workArea.width) ) {
				if (createdWindow.outerBounds.top < 0) {
					createdWindow.outerBounds.top = 0;
				}
				if (createdWindow.outerBounds.top > display.workArea.top + display.workArea.height) {
					createdWindow.outerBounds.top = display.workArea.top + display.workArea.height - WIN_MIN_HEIGHT;
				}
			}
		}
	});
}

function show(){
	if (!createdWindow)return;
	var inh = 450;

	createdWindow.outerBounds.height = 450;
	createdWindow.outerBounds.top -= inh - WIN_MIN_HEIGHT;
	
	normalize();
}

function hide(){
	if (!createdWindow)return;
	var inh = createdWindow.outerBounds.height;

	createdWindow.outerBounds.height = WIN_MIN_HEIGHT;
	createdWindow.outerBounds.top += inh - WIN_MIN_HEIGHT;

	normalize();
}
function storage_set(key, value) {
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
				try{
					callback(JSON.parse(xhr.responseText));
				} catch (e) {}
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
			if (data.failed){
				self.init();
				return;
			}
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
					
					if(!createdWindow) {
						createWindow();

						window.setTimeout(function(){

							chrome.runtime.sendMessage({
								action: "messages", 
								messages: m,
							}, function(response) {});

						}, 3000);
					} else {
						chrome.runtime.sendMessage({
							action: "messages", 
							messages: m,
						}, function(response) {});
					}
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

	if (request.action == "attention"){
		if (request.m){
			createdWindow.drawAttention();
		} else {
			createdWindow.clearAttention();
		}
	}
});