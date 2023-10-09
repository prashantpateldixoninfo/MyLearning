const express = require("express");
const path = require("path");
const app = express();
const port = 8080;

// For serving static files
app.use('/static', express.static('static'));

// Set the template engine as pug
app.set('view engine', 'pug');

// Set the views directory
app.set('views', path.join(__dirname, 'views'));

// Our pug demo endpoint
app.get("/demo", (req, resp) => {
    resp.status(200).render('demo', { title: 'Hi Prashant', message: 'Hello Prashant thanks for telling me about PUG :)' });
});

app.get("/", (req, resp) => {
    resp.status(200).send("This is home page of my first express app with Prashant");
});

app.get("/about", (req, resp) => {
    resp.send("This is about page of my first express app with Prashant");
});

app.post("/about", (req, resp) => {
    resp.send("This is POST about page of my first express app with Prashant");
});

app.listen(port, () => {
    console.log(`The application started successfully on port ${port}`);
})