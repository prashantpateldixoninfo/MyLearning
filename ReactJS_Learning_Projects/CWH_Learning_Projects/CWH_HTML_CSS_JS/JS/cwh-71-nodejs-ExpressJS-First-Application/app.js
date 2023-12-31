const express = require("express");

const app = express();
const port = 8080;

app.get("/", (req, resp) => {
    resp.status(200).send("This is home page of my first express app with Prashant");
});

app.get("/about", (req, resp) => {
    resp.send("This is about page of my first express app with Prashant");
});

app.post("/about", (req, resp) => {
    resp.send("This is POST about page of my first express app with Prashant");
});

app.listen(port, ()=> {
    console.log(`The application started successfully on port ${port}`);
})