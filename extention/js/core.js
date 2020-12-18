$(document).ready(function() {
	var time_out = 15 * 60 * 1000;
	var paramsString = document.location.search;
	var searchParams = new URLSearchParams(paramsString);
	var videoId = searchParams.get("v");
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
		var element = document.getElementsByClassName("video-stream html5-main-video")[0];
		let timerId = setInterval(function(){
			for(var index in result){
				var subtitle = result[index];
				var now_time = element.currentTime;
				if(subtitle[0] <= now_time && now_time < subtitle[0] + subtitle[1]) element.currentTime = subtitle[0] + subtitle[1];
			}
		}, 10);
		setTimeout(function(){
			clearInterval(timerId);
			console.log('time_out');
		}, time_out);
	});
});
