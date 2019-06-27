function sendMessage() {
  var inputText = document.getElementById("input-text");

  if (inputText.value == "") {
    alert("You can not send empty query!");
    return;
  }

  getResponseFromEs(inputText.value);
  inputText.value = "";
}

function getResponseFromEs(inputText) {
  var xhr = new XMLHttpRequest();
  var url = "http://localhost:6789/search";
  var params = new FormData();
  params.append("keyword", inputText);

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if ((xhr.status >= 200 && xhr.status < 300) || xhr.status == 304) {
        // alert("Fetching results from Elasticsearch...");
        var respMsg = JSON.parse(xhr.response);
        console.log(respMsg);
        showResp(respMsg);
      }
    }
  };
  xhr.open("POST", url, true);
  xhr.send(params);
}

function showResp(respMsg) {
  var resultArea = document.getElementById("result-area");
  resultArea.innerHTML = "";
  for (var i in respMsg) {
    var curRes = respMsg[i]["highlight"];
    var sourceVideo = respMsg[i]["video_name"];
    var startTime = respMsg[i]["start_timestamp"];

    var showRes = `
			<li class="result-item">
				<div>
					Source video: <b> ${sourceVideo} </b>
				</div>
				<div>
					Appeared timestamp: ${startTime}
				</div>
				<div>
					Content detail:
					<br>
					${curRes}
				</div>
			</li>
		`;

    resultArea.innerHTML += showRes;
  }
}

function enterPress(e) {
  var e = e || window.event;
  if (e.keyCode == 13) {
    sendMessage();
  }
}
