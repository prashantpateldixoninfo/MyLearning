const express = require("express");
const path = require("path");   
const app = express();
const port = 8080;
const bodyparser = require("body-parser");
var mongoose = require("mongoose");

// Connect to mongoose
mongoose.connect('mongodb://127.0.0.1/contactDance', {useNewUrlParser: true});

// Define mongoose schema
var contactSchema = new mongoose.Schema({
    name: String,
    phone: String,
    email: String,
    address: String,
    desc: String
  });

var Contact = mongoose.model('Contact', contactSchema);

// EXPRESS SPECIFIC STUFF
app.use('/static', express.static('static'));
app.use(express.urlencoded());

// PUG SPECIFIC STUFF
app.set('view engine', 'pug'); // Set the template engine as pug 
app.set('views', path.join(__dirname, 'views')); // Set the views directory

// ENDPOINTS
app.get('/', (req, resp) => {
    const params = {};
    // resp.status(200).render('index.pug', params);
    resp.status(200).render('home.pug', params);
})

app.get('/contact', (req, resp) => {
    const params = {};
    // resp.status(200).render('index.pug', params);
    resp.status(200).render('contact.pug', params);
})

app.post('/contact', (req, resp) => {
    var myData = new Contact(req.body);
    myData.save().then(() => {
        resp.send("This item has been saved to database")
    }).catch(() => {
        resp.status(400).send("Item was not saved to the database");
    });
    console.log("Receive Parameter = ", myData);
    // resp.status(200).render("contact.pug");
})


// START THE SERVER
app.listen(port, () => {
    console.log(`The application started successfully on port ${port}`);
})