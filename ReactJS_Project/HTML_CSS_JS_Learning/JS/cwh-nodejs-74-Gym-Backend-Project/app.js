const express = require("express");
const path = require("path");
const fs = require("fs");
const app = express();
const port = 8080;

// EXPRESS SPECIFIC STUFF
app.use('/static', express.static('static'));
app.use(express.urlencoded());

// PUG SPECIFIC STUFF
app.set('view engine', 'pug'); // Set the template engine as pug 
app.set('views', path.join(__dirname, 'views')); // Set the views directory

// ENDPOINTS
app.get('/', (req, resp) => {
    const con = "This is best content available on the internet, therefore use wisely"
    const params = { 'title': 'Pubg is not good for kids', "content": con };
    resp.status(200).render('index.pug', params);
})

app.post('/', (req, resp) => {
    // console.log(req.body);
    name = req.body.name;
    age = req.body.age;
    gender = req.body.gender;
    address = req.body.address;
    more = req.body.more;

    let outputToWrite = `The name of the client is ${name}, ${age} years old, ${gender}, reside at ${address}. More about hi/her: ${more}`;
    fs.writeFileSync('output.txt', outputToWrite);
    
    const params = { 'message': 'Your message is saved successfully' };
    resp.status(200).render('index.pug', params);
})

// START THE SERVER
app.listen(port, () => {
    console.log(`The application started successfully on port ${port}`);
})