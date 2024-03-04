// You have to write a Node.js program to clear clutter inside of a directory and organize the contents of that directory into different folders

// for example, these files become:

// 1. name.jpg
// 2. name.png
// 3. this.pdf
// 4. harry.zip
// 5. Rohan.zip
// 6. cat.jpg
// 7. harry.pdf

// this:
// jpg/name.jpg, jpg/cat.jpg
// png/name.png
// pdf/this.pdf pdf/harry.pdf
// zip/harry.zip zip/Rohan.zip

import fs from "fs";
import fsp from "fs/promises";
import path from "path";

// Get the path of files
const basepath = "C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-91-Exercise15-Clear-the-Clutter\\TestFolder";

let files = await fsp.readdir(basepath);

for (const item of files) {
    let ext = item.split(".").pop();

    if (fs.existsSync(path.join(basepath, ext))) {
        fs.copyFile(path.join(basepath, item), path.join(basepath, ext, item), (err) => {
            if (err) {
                console.error("Error copying file:", err);
            } else {
                console.log("File copied to directory successfully.");
            }
        });
    } else {
        fsp.mkdir(path.join(basepath, ext));
        fs.copyFile(path.join(basepath, item), path.join(basepath, ext, item), (err) => {
            if (err) {
                console.error("Error copying file:", err);
            } else {
                console.log("File copied to directory successfully.");
            }
        });
    }
}
