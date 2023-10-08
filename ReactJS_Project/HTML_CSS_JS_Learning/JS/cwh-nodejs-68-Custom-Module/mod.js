console.log("This is Module(mod.js)");

function average(arr) {
    let sum = 0;
    arr.forEach(element => {
        sum += element;
    });
    return sum / arr.length;
}

module.exports = {
    avg: average,
    name: "Prashant",
    repo: "GitHub"
}

module.exports.name = "Prashant";
