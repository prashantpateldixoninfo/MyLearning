const mongoose = require("mongoose");

const EmployeeSchema = new mongoose.Schema({
    name: String,
    salary: Number,
    language: String,
    city: String,
    isManager: Boolean,
});

const EmployeeDB = mongoose.model("EmployeeDB", EmployeeSchema);
module.exports = EmployeeDB;
