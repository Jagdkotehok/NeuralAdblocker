$(document).ready(function() {
	var paramsString = document.location.search;
	var searchParams = new URLSearchParams(paramsString);
	var videoId = searchParams.get("v");
	alert(videoId);
	$.ajax({
		url: "http://localhost:8080/get?v=" + videoId,
		dataType: "json"
	}).done(function (msg) {
		console.log(msg);
	});
});
