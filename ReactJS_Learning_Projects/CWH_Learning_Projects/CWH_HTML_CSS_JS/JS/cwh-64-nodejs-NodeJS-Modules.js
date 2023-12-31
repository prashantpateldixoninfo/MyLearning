const fs = require("fs");
let text = fs.readFileSync("myfile1.txt", "utf-8");
text = text.replace("Prashant", "P Patel");

console.log("The content of file is --> ");
console.log(text);

console.log("Creating a new file...");
fs.writeFileSync("myfile2.txt", text);
