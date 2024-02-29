import fs from "fs/promises";

let a = await fs.readFile("C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-87-Working-with-Files\\prashant.txt");

let b = await fs.appendFile(
    "C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-87-Working-with-Files\\prashant.txt",
    "\n\n\n\nthis is amazing promise"
);
console.log(a.toString(), b);
