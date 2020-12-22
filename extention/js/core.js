var result = [];
var parts = [];
var INF = 1000000000;
$(document).ready(function() {
	setTimeout(function(){
		var x = document.getElementsByTagName("ytd-macro-markers-list-item-renderer");
		if (typeof(x) !== "undefined"){
			var yy = [];
			var zz = [];
			for (var i = 0; i < x.length; ++i) {
				var y = x[i].getElementsByClassName("style-scope ytd-macro-markers-list-item-renderer")[5].textContent;
				var z = x[i].getElementsByClassName("style-scope ytd-macro-markers-list-item-renderer")[6].textContent;
				yy.push(y);
				var time = z.split(":");
				zz.push(parseInt(time[0]) * 60 * 1000 + parseInt(time[1]) * 10);
			}
			console.log(yy);
			console.log(zz);
			zz.push(INF);
			/*for(var __index = 0; __index < yy.length; ++__index){
				setTimeout(() => {
					$.ajax({
						url: "http://localhost:8080/ad?text=" + yy[__index],
						dataType: "json"
					}).done(function (msg) {
						console.log('Answer for ' + __index);
						var ans = msg['subtitle']
						if(ans === 1) parts.push([zz[__index] / 1000, (zz[__index + 1] - zz[__index]) / 1000]);
					});
				}, 10 * 1000 * (__index + 1));
			}*/
			setTimeout(() => {
				$.ajax({
					url: "http://localhost:8080/ad?text=" + yy[6],
					dataType: "json"
				}).done(function (msg) {
					var ans = msg['subtitle']
					if(ans === 1) parts.push([zz[6] / 1000, (zz[6 + 1] - zz[6]) / 1000]);
				});
			}, 10 * 1000);
		}

	}, 2000);
	var time_out = 15 * 60 * 1000;
	var paramsString = document.location.search;
	var searchParams = new URLSearchParams(paramsString);
	var videoId = searchParams.get("v");
	$.ajax({
		url: "http://localhost:8080/get?v=" + videoId,
		dataType: "json"
	}).done(function (msg) {
		for(var subtitle in msg['subtitles']){
			var now = msg['subtitles'][subtitle];
			result.push([now['start'], now['dur']]);
		}
		console.log(result);
		var element = document.getElementsByClassName("video-stream html5-main-video")[0];
		let timerId = setInterval(function(){
			for(var index in parts){
				var subtitle = parts[index];
				var now_time = element.currentTime;
				if(subtitle[0] <= now_time && now_time < subtitle[0] + subtitle[1]){
					element.currentTime = subtitle[0] + subtitle[1];
					console.log("-> 1 " + now_time);
				}
			}
			for(var index in result){
				var subtitle = result[index];
				var now_time = element.currentTime;
				if(subtitle[0] <= now_time && now_time < subtitle[0] + subtitle[1]){
					element.currentTime = subtitle[0] + subtitle[1];
					console.log("-> 2 " + now_time);
				}
			}
		}, 10);
		setTimeout(function(){
			clearInterval(timerId);
			console.log('time_out');
		}, time_out);
	});
});
setTimeout(function(){
	console.log(parts);
	console.log(result);
}, 60 * 1000);
