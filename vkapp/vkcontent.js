window.setInterval(function(){
	chrome.runtime.sendMessage({action: "title", data: document.getElementsByTagName('title')[0].innerHTML}, function(response) {
	  	
	});
}, 1000);
