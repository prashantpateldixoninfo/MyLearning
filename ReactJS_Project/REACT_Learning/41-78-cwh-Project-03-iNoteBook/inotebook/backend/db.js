const mongoose = require("mongoose");

const mongoURI = "mongodb://127.0.0.1:27017/inotebook?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false";

const connectToMongo = async () => {
  await mongoose.connect(mongoURI).then(
    () => {
      console.log("Connected to MongoDB Successfully");
    },
    err => {
      console.log(`Failed to Connect MongoDB due to ${err}`);
    }
  );
};

module.exports = connectToMongo;
