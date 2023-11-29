const express = require("express");
const router = express.Router();
const fetchuser = require("../middleware/fetchuser");
const Note = require("../models/Note");
const { body, validationResult } = require("express-validator");

// ROUTE 1: Get All the notes using: GET "/api/notes/getuser". Login required.
router.get("/fetchallnotes", fetchuser, async (req, res) => {
  try {
    const notes = await Note.find({ user: req.user.id });
    res.json(notes);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Internal Server Error " + error.message);
  }
});

// ROUTE 2: Add a new Note using: POST "/api/notes/addnote". Login required.
router.post("/addnote", fetchuser, [body("title", "Enter a valid title").isLength({ min: 3 }), body("description", "Enter a valid description").isLength({ min: 5 })], async (req, res) => {
  try {
    // If there are errors, return Bad request and the errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { title, description, tag } = req.body;

    const note = new Note({
      title,
      description,
      tag,
      user: req.user.id,
    });
    const saveNotes = await note.save();
    res.json(note);
  } catch (error) {
    console.log(error.message);
    res.status(500).send("Internal Server Error " + error.message);
  }
});

module.exports = router;
