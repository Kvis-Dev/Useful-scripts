chrome.app.window.create('vk.html',{
	id: 'vk',
	height: 450,
	width: 300,
	focused: true,
	alwaysOnTop: true,
	frame: 'none',
});



	/*
, function(tt){
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
	}
	*/