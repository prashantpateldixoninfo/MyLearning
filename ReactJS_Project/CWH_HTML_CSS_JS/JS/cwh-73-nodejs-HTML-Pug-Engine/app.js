const express = require("express");
const path = require("path");
const app = express();
const port = 8080;

// EXPRESS SPECIFIC STUFF
app.use('/static', express.static('static'));

// PUG SPECIFIC STUFF
app.set('view engine', 'pug'); // Set the template engine as pug 
app.set('views', path.join(__dirname, 'views')); // Set the views directory

// ENDPOINTS
app.get('/', (req, resp) => {
    const con = "This is best content available on the internet, therefore use wisely"
    const params = { 'title': 'Pubg is not good for kids', "content": con };
    resp.status(200).render('index.pug', params);
})

// START THE SERVER
app.listen(port, () => {
    console.log(`The application started successfully on port ${port}`);
})