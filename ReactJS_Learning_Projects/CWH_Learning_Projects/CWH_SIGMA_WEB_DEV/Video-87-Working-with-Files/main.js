const fs = require("fs");
// const fs = require("fs/promises")
// console.log(fs);

console.log("starting");
// fs.writeFileSync("prashant.txt", "Prashant is a good boy");
fs.writeFile("C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-87-Working-with-Files\\prashant2.txt", "Prashant is a good boy2", () => {
    console.log("done");
    fs.readFile("C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-87-Working-with-Files\\prashant2.txt", (error, data) => {
        console.log(error, data.toString());
    });
});

fs.appendFile("C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-87-Working-with-Files\\prashant.txt", "Prashantrobot", (e, d) => {
    console.log(e, d);
});

console.log("ending");
