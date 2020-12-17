console.log("ABBA");
alert("Привет");
setTimeout(
	function(){
		document.getElementsByClassName("style-scope ytd-video-primary-info-renderer")[0].textContent = "AAAAAAAA";
	}, 3000
)


$(document).ready(function() {
  $.ajax({
    url: "http://localhost:8080/get?v=1",
    dataType: "json"
  }).done(function (msg) {
    console.log(msg);
  });
});
