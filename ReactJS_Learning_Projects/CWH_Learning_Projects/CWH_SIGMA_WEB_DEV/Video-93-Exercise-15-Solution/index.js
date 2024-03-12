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

import fs from "fs/promises";
import fsn from "fs";
import path from "path";

const basepath = "C:\\DixonProject\\MyLearning\\ReactJS_Learning_Projects\\CWH_Learning_Projects\\CWH_SIGMA_WEB_DEV\\Video-93-Exercise-15-Solution";
const migrationpath = "C:\\Users\\DXN4263\\Desktop\\DeleteMe";

let files = await fs.readdir(basepath);
console.log(files);
for (const item of files) {
    console.log("running for ", item);
    let ext = item.split(".")[item.split(".").length - 1];
    if (ext != "js" && ext != "json" && ext != "gitignore" && item.split(".").length > 1) {
        if (fsn.existsSync(path.join(migrationpath, ext))) {
            // Move the file to this directory if its not a js, json or gitignore file
            fs.copyFile(path.join(basepath, item), path.join(migrationpath, ext, item));
        } else {
            fs.mkdir(path.join(migrationpath, ext));
            fs.copyFile(path.join(basepath, item), path.join(migrationpath, ext, item));
        }
    }
}
