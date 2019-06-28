const videoPath = [
  "assets/videos/DynDNS and OpenDNS/GMT20190530-125057_Ian-Hadfie_2560x1440.mp4",
  "assets/videos/AD GPO to Disable Accounts : WSUS General Info/GMT20181010-185000_Ian-Hadfie_1920x1200.mp4",
  "assets/videos/Adaptive Microsegmentation/GMT20190118-000728_Kunjal-Rat_1920x1080.mp4",
  "assets/videos/Publishing upgrade bundles to S3/GMT20190207-163402_Publishing_1680x1050.mp4",
  "assets/videos/Containers for DevOps/GMT20181019-183347_HCS-DevOps_1920x1080.mp4",
  "assets/videos/Thycotic Secret Server/GMT20180927-150424_Thycotic-S_1920x1080.mp4",
  "assets/videos/Open Discussion with India Ops/GMT20190610-130416_Discussion_1920x1222.mp4",
  "assets/videos/Robot Code Walk Through/GMT20181031-163636_Robot-Code_1680x1050.mp4",
  "assets/videos/Scope Dashboard/GMT20181217-220454_Carolyn-Ma_1920x1080.mp4",
  "assets/videos/Networking Discussion/GMT20190610-170356_Ian-Hadfie_2560x1440.mp4",
  "assets/videos/An Introduction to the Platform/GMT20180822-180150_Q-Hoang-s-_1920x1200.mp4",
  "assets/videos/Kubernetes on Hydra Primer/GMT20190613-200350_Brownbag-S_1596x720.mp4",
  "assets/videos/Log Collection Slack Integration Demo/GMT20180928-210239_Log-Collec_1680x1050.mp4",
  "assets/videos/Panorama IDS System by Palo Alto Networks/GMT20190606-130525_Parban-Cha_2560x1440.mp4",
  "assets/videos/An Introduction to Hydra/GMT20181024-210141_Vivien-Rua_1920x1080.mp4",
  "assets/videos/Hulk Feature - On Demand Process Handling/GMT20190411-033308_Hulk-Featu_1680x1050.mp4"
];

window.onload = function() {
  var videoArea = document.getElementById("video-area");
  for (var i = 0; i < 5; i += 1) {
    var videoItem = `
      <div class="list-group-item list-group-item-dark">
        ${videoPath[i].split("/")[2]}
      </div>
      <div class="list-group-item">
        <video width="400" height="250" controls>
          <source
            src="${videoPath[i]}"
            type="video/mp4"
          />
        </video>
      </div>
    `;
    videoArea.innerHTML += videoItem;
  }
};

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
        // console.log(respMsg);
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
    var videoName = respMsg[i]["video_name"];
    var timeList = respMsg[i]["time_list"];
    // console.log(timeList);
    var videoTitleBar = `
      <li class="list-group-item list-group-item-primary">
        <div>
          Source video: <b> ${videoName} </b>
        </div>
      </li>
    `;
    resultArea.innerHTML += videoTitleBar;

    for (var j in timeList) {
      var curRes = timeList[j]["highlight"];
      var startTime = timeList[j]["start_timestamp"];

      var showRes = `
        <li 
          onclick="goToVideo(id)"
          class="list-group-item list-group-item-action result-item"
          id="${videoName}##${startTime}"
        >      
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

    // resultArea.addEventListener(
    //   "mousedown",
    //   function(event) {
    //     var curId = event.target.id;
    //     console.log(curId);
    //   },
    //   false
    // );
  }
}

function goToVideo(idStr) {
  var videoArea = document.getElementById("video-area");

  var videoName = idStr.split("##")[0];
  var timeStamp = timeToSec(idStr.split("##")[1]);
  var currentVideoItem = "";
  for (var i in videoPath) {
    if (videoPath[i].includes(videoName)) {
      var currentVideoPath = videoPath[i] + "#t=" + timeStamp;
      console.log(currentVideoPath);
      currentVideoItem = `
      <div class="list-group-item list-group-item-action">
        <video width="500" height="400" controls>
          <source
            src="${currentVideoPath}"
            type="video/mp4"
          />
        </video>
        ${videoPath[i].split("/")[2]}
      </div>
      `;
    }
  }

  videoArea.innerHTML = currentVideoItem;
}

function timeToSec(timeStamp) {
  var hour = timeStamp.split(":")[0];
  var minute = timeStamp.split(":")[1];
  var second = timeStamp.split(":")[2].split(".")[0];
  return Number(hour * 3600) + Number(minute * 60) + Number(second);
}

function enterPress(e) {
  var e = e || window.event;
  if (e.keyCode == 13) {
    sendMessage();
  }
}
