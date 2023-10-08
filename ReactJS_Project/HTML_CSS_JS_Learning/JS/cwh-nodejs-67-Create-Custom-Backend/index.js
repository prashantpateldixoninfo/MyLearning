const http = require('http');
const fs = require('fs');

const hostname = '127.0.0.1';
const port = 3000;

const home = fs.readFileSync('./index.html');
const about = fs.readFileSync('./about.html');
const services = fs.readFileSync('./services.html');
const contact = fs.readFileSync('./contact.html');


const server = http.createServer((req, resp) => {
    console.log(req.url);
    url = req.url;

    resp.statusCode = 200;
    resp.setHeader('content-type', 'text/html');

    if (url == '/' || url == '/home') {
        resp.end(home);
    }
    else if (url == '/about') {
        resp.end(about);
    }
    else if (url == '/services') {
        resp.end(services);
    }
    else if (url == '/contact') {
        resp.end(contact);
    }
    else {
        resp.statusCode = 404;
        resp.end("<h1>404 not found</h1>");
    }
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});