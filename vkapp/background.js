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

function show(){
	var inh = 450;

	createdWindow.outerBounds.height = 450;
	createdWindow.outerBounds.top -= inh - 30;
}

function hide(){
	var inh = createdWindow.outerBounds.height;

	createdWindow.outerBounds.height = 30;
	createdWindow.outerBounds.top += inh - 30;
}

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