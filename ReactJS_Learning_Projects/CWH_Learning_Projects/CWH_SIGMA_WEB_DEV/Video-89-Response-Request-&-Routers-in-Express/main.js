const express = require("express");
const blog = require("./routes/blog");
const shop = require("./routes/shop");

const app = express();
const port = 3000;

app.use(express.static("public"));
app.use("/blog", blog);
app.use("/shop", shop);

app.get("/", (req, res) => {
    console.log("Hey its a get request");
    res.send("Hello World GET");
}).post("/", (req, res) => {
    console.log("Hey its a post request");
    res.send("Hello World POST");
});

app.put("/", (req, res) => {
    console.log("Hey its a put request");
    res.send("Hello World PUT");
});

app.get("/index", (req, res) => {
    console.log("Hey its index");
    res.sendFile("templates/index.html", { root: __dirname });
});

app.get("/api", (req, res) => {
    res.json({ a: 1, b: 2, c: 3, d: 4, name: ["harry", "jerry"] });
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
