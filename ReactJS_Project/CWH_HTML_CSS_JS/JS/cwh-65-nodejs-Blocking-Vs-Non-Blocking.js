// Synchronous or blocking
// - line by line execution

// Asynchronous or non-blocking
// - line by line execution not guaranteed
// - callbacks will fire

const fs = require("fs");

fs.readFile("myfile1.txt", "utf-8", (err, data) => {
    if (data)
        console.log("Data is ==> ", data);
    if (err)
        console.log("Error is ==> ", err);
});

console.log("This is a message");