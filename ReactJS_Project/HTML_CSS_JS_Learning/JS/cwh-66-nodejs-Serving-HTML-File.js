const http = require('http');
const fs = require('fs');
const fileContent = fs.readFileSync('../CSS/tutorial-61_JS_Math_Objects.html');

const server = http.createServer((req, resp) => {
    resp.writeHead(200, { 'content-type': 'text/html' });
    resp.end(fileContent);
});

server.listen(8000, '127.0.0.1', () => {
    console.log("Listening on port 8000");
});
