var w = document.getElementById('webview');

var at = '';

function storage_set(key, value) {

	var dset = {};
	dset[key] = value;
	
	chrome.storage.local.set(dset, function() {
	});
}


w.addEventListener('loadstop', function(e) {
	if (w.src.indexOf('access_token') > 0) {
		at = w.src.split('access_token=')[1].split('&')[0];
		storage_set('vk_api', at);
	}
});


