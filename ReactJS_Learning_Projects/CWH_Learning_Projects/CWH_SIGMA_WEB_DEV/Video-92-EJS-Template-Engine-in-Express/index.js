const express = require("express");
const app = express();
const port = 3000;

app.set("view engine", "ejs");

// https://github.com/mde/ejs/wiki/Using-EJS-with-Express

app.get("/", (req, res) => {
    let siteName = "Adidas";
    let searchText = "Search Now";
    let arr = ["Hello", "EveryOne", 31, 91];
    res.render("index", { siteName: siteName, searchText: searchText, arr, root: __dirname });
});

app.get("/blog/:slug", (req, res) => {
    let blogTitle = "Adidas why and when";
    let blogContent = "It's a very good brand";
    res.render("blogpost.html", { blogTitle: blogTitle, blogContent: blogContent });
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
