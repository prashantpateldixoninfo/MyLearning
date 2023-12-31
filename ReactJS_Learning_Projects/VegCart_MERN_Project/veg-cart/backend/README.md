## Backend Code of Express Node and MongoDB

### `Install express and nodemon library`

```
npm install express
npm install --save-dev nodemon
```

### `Add the code of expressJS to lauch the application and start under veg-cart\backend> folder`

```
nodemon index.js
```

### `Install the mongoose library`

```
npm install mongoose
```

### `Create the db.js file and give the MongoDB path for connection`

### `Create the Schema/template for user, which will store the user data(schema) in MongoDB`

### `Install express-validator, bcrypt and jsonwebtoken`

```
npm install express-validator
npm install bcrypt
npm install jsonwebtoken
```

### `Write the code in auth.js file regarding the 'createuser' route path and add the route path mapping in index.js file.`

### `Use ThunderClient/Postman to test the Dabase creation.`

```
POST: http://localhost:5000/api/auth/createuser
BODY: {
    "name": "Prashant",
    "email": "prashant@buyer.com",
    "password": "12345",
    "user_type": "buyer"
}
RESPONSE: {
    "success": true
}
```

### `Install cors library, During GUI testing, policy restrict to pass the request to server. After cors instalaltion, test the Signup feature through browser(ReactJS code).`

```
Access to fetch at 'http://localhost:5000/api/auth/createuser' from origin 'http://localhost:3000' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.

npm install cors
```

### `Add the script('both') in 'package.json' file to start both frontend(ReactJS) and backend(NodeJS) together on single terminal.First install concurrently library And then run as 'npm run both' from frontend.`

```
npm install concurrently

"scripts": {
    ...,
    "both": "concurrently \"npm run start\" \"nodemon backend/index.js\""
}
```

### `Write the user login code in auth.js file. Create the auth-token for login session and store the suth-token into localStorage of browser`

### `Use ThunderClient/Postman to test login.`

```
POST: http://localhost:5000/api/auth/login
BODY: {
    "email": "prashant@buyer.com",
    "password": "12345",
}
RESPONSE: {
    "success": true,
    "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU4ZDAzNjliOGQxMmIyZWE2ZGMxYWM0In0sImlhdCI6MTcwMzc0MTg3OX0.QCpRR4fbfIIT0NjMauJJxBrAHzHJX85yMAXSk-Kqrq0"

}
```

### `Added user_type in login response, therefore application can decide the page`

```
RESPONSE: {
    "success": true,
    "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU4ZDAzNjliOGQxMmIyZWE2ZGMxYWM0In0sImlhdCI6MTcwMzc0MTg3OX0.QCpRR4fbfIIT0NjMauJJxBrAHzHJX85yMAXSk-Kqrq0",
    "user_type": "seller"
}
```
