const mongoose = require("mongoose");
const { Schema } = mongoose;

const UserSchema = new Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
    },
    password: {
        type: String,
        required: true,
    },
    user_type: {
        type: String,
        required: true,
    },
    date: {
        type: Date,
        default: Date.now,
    },
});

// Here, 'user' is the model name.
// In Mongoose, the model name is often used to infer the collection name in MongoDB.
// By default, Mongoose pluralizes the model name to determine the collection name.
// In this case, the collection name would likely be 'users'.
const User = mongoose.model("user", UserSchema);
// User.createIndexes();
module.exports = User;
