var w = document.getElementById('webview');

var at = '';




w.addEventListener('loadstop', function(e) {
	if (w.src.indexOf('access_token') > 0) {
		at = w.src.split('access_token=')[1].split('&')[0];

		chrome.storage.local.set({'vk_api' : at}, function() {
			window.close();
		});
	}
});


