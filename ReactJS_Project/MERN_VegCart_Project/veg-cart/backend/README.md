## Backend Code of Express Node and MongoDB

### Install express and nodemon library

    `npm install express`
    `npm install --save-dev nodemon`

### Add the code of expressJS to lauch the application and start under veg-cart\backend> folder

    `nodemon index.js`

### Install the mongoose library

    `npm install mongoose`

### Create the db.js file and give the MongoDB path for connection

### Create the Schema/template for user, which will store the user data(schema) in MongoDB

### Install express-validator, bcrypt and jsonwebtoken

    `npm install express-validator`
    `npm install bcrypt`
    `npm install jsonwebtoken`

### Write the code in auth.js file regarding the 'createuser' route path and add the route path mapping in index.js file.

### Use ThunderClient/Postman to test the Dabase creation.

    `POST: http://localhost:5000/api/auth/createuser`
    `BODY: {
        "name": "Amol",
        "email": "amol.gadekar@dixoninfo.com",
        "password": "12345",
        "user_type": "buyer"
    }`
    `RESPONSE: {
        "success": true,
        "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU4YmY0OTIyMzg4NmJlYmEyMmUxMGRlIn0sImlhdCI6MTcwMzY3MDkzMH0.jXNB2YKQd6DjYlNff9ReE4NJDybwb9PjhealDaIrDE0"
    }`
