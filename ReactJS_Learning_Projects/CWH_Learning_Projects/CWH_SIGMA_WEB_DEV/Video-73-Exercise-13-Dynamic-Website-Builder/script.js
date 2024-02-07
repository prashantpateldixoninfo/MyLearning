function createCard(title, cName, views, monthsOld, duration, thumbnail) {
    // Create and Append card class
    let divCardTag = document.createElement("div"); // <div></div>
    divCardTag.setAttribute("class", "card"); // <div class="card"></div>
    document.querySelector(".container").appendChild(divCardTag); // <div class="container"><div class="card"></div></div>

    // Create and Append text tag to card class
    let textTag = document.createElement("text"); // <text></text>
    document.querySelector(".card").appendChild(textTag); // <div class="container"><div class="card"><text></text></div></div>
    textTag.innerHTML = duration; // <div class="container"><div class="card"><text>32:10</text></div></div>

    // Create and Append content class
    let divContentTag = document.createElement("div"); // <div></div>
    divContentTag.setAttribute("class", "content"); // <div class="content"></div>
    document.querySelector(".container").appendChild(divContentTag); // <div class="container"><div class="card"></div></div>

    // Create and Append mytitle class to content class
    let divTitleTag = document.createElement("div");
    divTitleTag.setAttribute("class", "mytitle");
    document.querySelector(".content").appendChild(divTitleTag);
    divTitleTag.innerHTML = `${title}`;

    // Create and Append mytitle class to content class
    let divStatsTag = document.createElement("div");
    divStatsTag.setAttribute("class", "mystats");
    document.querySelector(".content").appendChild(divStatsTag);
    divStatsTag.innerHTML = `${cName} | ${Math.floor(views / 1000)}K | ${monthsOld} months ago`;

    // CSS Style of container class
    let contStyle = document.querySelector(".container").style;
    contStyle.height = "140px";
    contStyle.width = "max-content";
    contStyle.backgroundColor = "black";
    contStyle.display = "flex";

    // CSS Style of card class
    let cardStyle = document.querySelector(".card").style;
    cardStyle.margin = "5px";
    cardStyle.height = "130px";
    cardStyle.width = "200px";
    cardStyle.backgroundImage = `url(${thumbnail})`;
    cardStyle.backgroundColor = "yellowgreen";
    cardStyle.borderRadius = "8px";

    // CSS Style of text tag of card class
    let textStyle = document.querySelectorAll(".card")[0].firstElementChild.style;
    textStyle.position = "absolute";
    textStyle.color = "white";
    textStyle.backgroundColor = "black";
    textStyle.opacity = "0.7";
    textStyle.borderRadius = "8px";
    textStyle.padding = "3px";
    textStyle.marginTop = "105px";
    textStyle.marginLeft = "155px";

    // CSS Style of content class
    let contentStyle = document.querySelector(".content").style;
    console.log(document.querySelectorAll(".content"));
    contentStyle.marginTop = "5px";
    contentStyle.height = "130px";
    contentStyle.width = "max-content";
    contentStyle.display = "flex";
    contentStyle.flexDirection = "column";

    // CSS Style of title tag of content class
    let titleStyle = document.querySelectorAll(".content")[0].firstElementChild.style;
    titleStyle.color = "white";
    titleStyle.fontFamily = "Baloo Bhai";
    titleStyle.fontSize = "x-large";
    titleStyle.fontWeight = "300";

    // CSS Style of stats tag of content class
    let statsStyle = document.querySelectorAll(".content")[0].lastElementChild.style;
    statsStyle.color = "grey";
    statsStyle.fontFamily = "Arial, Helvetica, sans-serif";
    statsStyle.fontSize = "small";
}

createCard(
    "Installing VS Code & How Websites Work | Sigma Web Development Course - Tutorial#1",
    "CodeWithPrashant",
    560000,
    7,
    "31:22",
    "https://i.ytimg.com/vi/tVzUXW6siu0/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLACwWOixJVrKLFindK92kYMgTcQbw"
);
