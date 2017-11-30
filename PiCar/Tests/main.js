
window.onload = () => {
    document.body.style.backgroundColor="black";
}

/*
Logic:
Control according to the key press
*/

document.addEventListener("keypress", function(event) {
    handleKeyPress(event, true);
});

document.addEventListener("keyup", function(event) {
    handleKeyPress(event, false);
});

function handleKeyPress(keyEvent, down) {
    keyEvent.preventDefault();
    console.log(keyEvent.keyCode);
    document.getElementById("status").innerText = keyEvent.keyCode;  
  }