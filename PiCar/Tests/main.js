
window.onload = () => {
    document.body.style.backgroundColor="black";
}

/*
Logic:
Control according to the key press
*/

//document.addEventListener("keypress", function(event) {  handleKeyPress(event, true); });


document.addEventListener("keyup", function(event) {handleKeyPress(event, false); });


function handleKeyPress(keyEvent, down) {
    keyEvent.preventDefault();
    console.log(keyEvent.keyCode);
    document.getElementById("status").innerText = keyEvent.keyCode;   

    // send ajax request
    loadDoc(keyEvent.keyCode);

}


function loadDoc(key_code) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        let jsn = JSON.stringify(JSON.parse(this.responseText), null, 3);  
        document.getElementById("response").innerHTML = `<pre>${jsn}</pre>`;
      }
    };
    xhttp.open("GET", `cmd/${key_code}`, true);
    xhttp.send();
  }
  