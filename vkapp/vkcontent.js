window.setInterval(function(){
	var m = 0;
	try{
		var tm = parseInt(document.querySelector('#header_msgs .mh_notify_counter').innerHTML);
		if (! isNaN(tm)){
			m = tm;
		}
	} catch(e){

	}

	chrome.runtime.sendMessage({
		action: "title", 
		data: document.getElementsByTagName('title')[0].innerHTML,
		messages: m,
	}, function(response) {
	  	
	});
}, 500);
