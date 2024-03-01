const express = require("express");
const app = express();
const port = 3000;
const blog = require("./routes/blog");
const fs = require("fs");

// app.use(express.static("public"))

app.use("/blog", blog);

// Middleware 1 - Logger for our application
app.use((req, res, next) => {
    console.log(req.headers);
    req.harry = "I am harry bhai";
    const date = new Date();
    fs.appendFileSync("logs.txt", `${date} is a ${req.method}\n`);
    console.log(`${date} is a ${req.method}`);
    // res.send("Hacked by Middlware 1")
    next();
});

// Middleware 2
app.use((req, res, next) => {
    console.log("m2");
    req.harry = "I am Rohan bhai";
    next();
});

app.get(
    "/user/:id",
    (req, res, next) => {
        // if the user ID is 0, skip to the next route
        if (req.params.id === "0") {
            next("route");
        }
        // otherwise pass the control to the next middleware function in this stack
        else {
            next();
        }
    },
    (req, res, next) => {
        // send a regular response
        res.send("regular");
    }
);

// handler for the /user/:id path, which sends a special response
app.get("/user/:id", (req, res, next) => {
    res.send("special");
});

app.get("/", (req, res) => {
    res.send("Hello World!");
});

app.get("/about", (req, res) => {
    res.send("Hello about!" + req.harry);
});

app.get("/contact", (req, res) => {
    res.send("Hello contact!");
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
