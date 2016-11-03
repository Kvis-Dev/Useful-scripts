var $ = function(id) {
	return document.getElementById(id);
};

var addWebview = function(src) {
	var w = $('webview');

	        w.addEventListener('newwindow', function(e) {
          e.preventDefault();
          // e.targetUrl contains the target URL of the original link click
          // or window.open() call: use it to open your own window to it.
          // Something to keep in mind: window.open() called from the
          // app's event page is currently (Nov 2013) handicapped and buggy
          // (e.g. it doesn't have access to local storage, including cookie
          // store). You can try to use it here and below, but be prepare that
          // it may sometimes produce bad results.
          // chrome.app.window.create(e.targetUrl);
          // chrome.tabs.create({
          // 	url:e.targetUrl,
          // });
          window.open(e.targetUrl);
        });


w.addContentScripts([{
		    name: 'myRule',
		    matches: ['https://vk.com/*'],
		    css: { files: ['smallvk.css'] },
		    js: { files: ['vkcontent.js'] },
		    run_at: 'document_start'
		}]);
	w.addEventListener('loadstop', function(e) {

		

		// w.insertCSS({
		// 	file: 'smallvk.css'
		// }, function() {console.log('ins')});


	});



	w.setAttribute('src', src);
};

window.onload = function() {
	addWebview('http://vk.com/im');
};

$('close').addEventListener('click', function(){
	window.close();
});


chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "title"){
		$('title').innerHTML = request.data;
	}
});