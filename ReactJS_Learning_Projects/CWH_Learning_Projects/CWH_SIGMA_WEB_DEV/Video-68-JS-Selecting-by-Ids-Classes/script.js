console.log("Harry");

// let boxes = document.getElementsByClassName("box")
// console.log(boxes)

// boxes[2].style.backgroundColor = "red"

// document.getElementById("redbox").style.backgroundColor = "red"

// document.querySelector(".box").style.backgroundColor = "green";
console.log(document.querySelectorAll(".box"));

document.querySelectorAll(".box").forEach((e) => {
    e.style.backgroundColor = "green";
});

console.log("matches -->", document.getElementsByTagName("div")[4].matches("#redbox"));
console.log("matches -->", document.getElementsByTagName("div")[3].matches("#redbox"));

console.log("closest -->", document.getElementsByTagName("div")[3].closest("#redbox"));
console.log("closest -->", document.getElementsByTagName("div")[3].closest(".container"));
console.log("closest -->", document.getElementsByTagName("div")[3].closest("html"));

console.log("contains -->", document.querySelector(".container").contains(document.querySelector("body")));
console.log("contains -->", document.querySelector("body").contains(document.querySelector(".container")));
