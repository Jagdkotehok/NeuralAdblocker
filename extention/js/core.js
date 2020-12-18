$(document).ready(function() {
	var paramsString = document.location.search;
	var searchParams = new URLSearchParams(paramsString);
	var videoId = searchParams.get("v");
	alert(videoId);
	$.ajax({
		url: "http://localhost:8080/get?v=" + videoId,
		dataType: "json"
	}).done(function (msg) {
		var result = [];
		for(var subtitle in msg['subtitles']){
			var now = msg['subtitles'][subtitle];
			result.push([parseFloat(now['start']), parseFloat(now['dur'])]);
		}
		console.log(result);
	});
});
