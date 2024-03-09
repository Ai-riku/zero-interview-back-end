// Function to check if the audio stream has ended every second
function checkAudioStream() {
    var audioCheck = setInterval(function() {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/transcript_complete', true);
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4) {
            if (xhr.status === 201) {
              console.log("Audio transcript complete");
              clearInterval(audioCheck);
              audioStreamEnded();
            }
          }
        };
        xhr.send();
      }, 1000); // 1 second
}

// Function to handle the audio stream end
function audioStreamEnded() {
    fetch('/transcription')
    .then(response => response.text())
    .then(data => {
        document.getElementById('transcript').innerText = data;
    });
}

checkAudioStream();