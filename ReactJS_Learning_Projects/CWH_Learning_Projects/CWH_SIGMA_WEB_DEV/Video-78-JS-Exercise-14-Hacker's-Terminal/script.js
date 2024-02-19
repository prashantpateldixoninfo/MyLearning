function messagedisplay(text) {
    setTimeout(function () {
        console.log(text);
        let pTag = document.createElement("p");
        pTag.innerText = `${text}...`;
        let contStyle = document.querySelector(".container").style;
        contStyle.color = "aliceblue";
        contStyle.fontSize = "larger";
        document.querySelector(".container").appendChild(pTag);
    }, 1000);
}

console.log("I am in setTimeout");

let text = ["Initializing Hacking", "Reading your Files", "Password files Detected", "Sending all passwords and personal files to server", "Cleaning up"];

let randomMS = Math.ceil(1 + Math.random() * 7) * 1000;
setInterval(() => {
    for (let i = 0; i < text.length; i++) {
        runMessage(text[i]);
    }
}, randomMS);

function runMessage(msg) {
    messagedisplay(msg);
}
