// Generate a dummy data in this format in a collection called employees in a db called company

// {
//     name: "Harry",
//     salary: 45000000,
//     language: "Python",
//     city: "New York",
//     isManager: true
// }

// Generate 10 such records when a button called generate data is clicked!
// Create an Express app with mongoose to acheive it
// Everytime the button is clicked, you should clear the collection

const express = require("express");
const app = express();
const mongoose = require("mongoose");
const EmployeeDB = require("./models/Employee");

const conn = mongoose.connect("mongodb://127.0.0.1:27017/employeedb");
const port = 3000;

app.set("view engine", "ejs");

const getRandom = (arr) => {
    let val = Math.floor(Math.random() * (arr.length - 1));
    return arr[val];
};

app.get("/", (req, res) => {
    res.render("index", { foo: "FOO" });
});

app.get("/generate", async (req, res) => {
    // Clear the collection Employee
    await EmployeeDB.deleteMany({});
    // Generate random data

    let names = ["Prashant", "Naman", "Rohini", "Rohit", "Riya", "Gaurav", "Srini"];
    let languages = ["Python", "Java", "Java Script", "C", "C++", "Golang", "TypeScript"];
    let cities = ["Hyderabad", "Delhi", "Mumbai", "Pune", "Banglore", "Indore", "Gurugram"];

    for (let index = 0; index < 10; index++) {
        let e = await EmployeeDB.create({
            name: getRandom(names),
            salary: Math.floor(Math.random() * 22000),
            language: getRandom(languages),
            city: getRandom(cities),
            isManager: Math.random() > 0.5 ? true : false,
        });
        // console.log(e);
    }

    res.render("index", { foo: "FOO" });
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
