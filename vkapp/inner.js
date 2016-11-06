var $ = function(id) {
	return document.getElementById(id);
};

var messages = 0;

function playSound(soundfile) {
	var a = new Audio();
	a.src = soundfile;
	a.autoplay = true;
};

var addWebview = function(src) {
	var w = $('webview');

	w.addEventListener('newwindow', function(e) {
		e.preventDefault();
		window.open(e.targetUrl);
	});

	w.addContentScripts([{
		name: 'myRule',
		matches: ['https://m.vk.com/*'],
		js: { files: ['vkcontent.js'] },
		run_at: 'document_start'
	}]);
	w.addEventListener('loadstop', function(e) {});

	w.setAttribute('src', src);
};

window.onload = function() {
	addWebview('http://m.vk.com/mail');
};

$('close').addEventListener('click', function(event){
	window.close();
	event.stopPropagation();
});

$('hide').addEventListener('click', function(event){
	chrome.runtime.sendMessage({action: "hide"}, function(response) {});
	event.stopPropagation();
	return false;
});

var md = 0;
document.querySelector('.titlebar').addEventListener('mousedown', function(event){
	md = event.timeStamp;
});

document.querySelector('.titlebar').addEventListener('mouseup', function(event){
	event.stopPropagation();
	if (event.timeStamp - md < 400) {
		chrome.runtime.sendMessage({action: "titleclick"}, function(response) {});
	}
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "title"){
		$('title').innerHTML = request.data;
	}

	if (request.action == "messages"){
		if (request.messages) {
			document.querySelector('.titlebar').classList.add('noisy');
		} else {
			document.querySelector('.titlebar').classList.remove('noisy');
		}

		if (messages < request.messages) {
			messages = request.messages;
			playSound('./notification.mp3');
		}

		messages = request.messages;
	}
});