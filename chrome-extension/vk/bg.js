var vkWind = null;
var msgsPrev = 0;
var msgs = 0;
var wid = 0;
var wtab = 0;

var nstr;

function is_int(mixed_var) {
	return mixed_var === +mixed_var && isFinite(mixed_var) && !(mixed_var % 1);
}

function playSound(soundfile) {
	var a = new Audio();
	a.src = soundfile;
	a.autoplay = true;
};
function doStuffWithDom(domContent) {
    console.log('I received the following DOM content:\n' + domContent);
}
function createWindow(){
	try {
		chrome.windows.remove(wid, function(){
			if (chrome.runtime.lastError) {}
		}); 
	} catch(e) {

	}

	chrome.windows.create({
		url: "https://m.vk.com/im", 
		type: 'panel',
		height: 450,
		width: 300,
		focused: true,
	}, function(tt){
		wtab = tt.tabs[0];
		wid = tt.id;

//		'<meta name="viewport" content="width=device-width, initial-scale=1">'
				

		//chrome.tabs.sendMessage(tab.id, {text: 'report_back'}, doStuffWithDom);
		console.log(tt.tabs)

		chrome.tabs.insertCSS(wtab.id, {file: 'vk.css'}, function (tab){
			if (chrome.runtime.lastError) {}
			console.log('sds',chrome.runtime.lastError);
		});

		chrome.tabs.insertCSS(wid, {file: 'vk.css'}, function (tab){
			if (chrome.runtime.lastError) {}
			console.log('sds',chrome.runtime.lastError);
		});

		

		chrome.windows.onFocusChanged.addListener(function(windowId){
			if (windowId == wid) {

				var chwin = chrome.windows.get(wid, {}, function(window__){
					
					if (window__.focused && window__.state == "minimized") {
						//chrome.windows.update(windowId, {state: 'maximized'}, function(){});
					} else if (window__.focused && window__.state == "maximized") {
						chrome.windows.update(windowId, {state: 'minimized'}, function(){});
					}

				});
			}
		});
	});
}

function notify(){
	playSound( chrome.extension.getURL('notification.mp3') );

	chrome.windows.update(wid, {
		drawAttention : true,
	}, function(){
		if (chrome.runtime.lastError) {
			createWindow();
		} 
	});
}

chrome.browserAction.onClicked.addListener(function () {
	createWindow();
});

function cfunc() {
	setTimeout(cfunc, 30000);
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "https://m.vk.com/im", true);
	xhr.setRequestHeader('Cache-Control', 'no-cache');
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			try{
				nstr = xhr.response.split('<li class="mmi_mail">')[1].split('</li>')[0].split('<em class="mm_counter">')[1].split('</em>')[0];
				msgs = parseInt(nstr);
			} catch(e) {
				msgs = 0;msgsPrev = 0;
				chrome.windows.update(wid, {
					drawAttention : false,
				}, function(){
					if (chrome.runtime.lastError) {
					} 
				});
				return;
			}
			if (msgsPrev < msgs) {
				notify();
			} 
			msgsPrev = msgs;
		}
	}
	xhr.send();
};

cfunc();

chrome.browserAction.setIcon({path: 'icon.png'});