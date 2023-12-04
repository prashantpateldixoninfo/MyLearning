import React, { useState } from "react";
import NoteContext from "./NoteContext";

const NoteState = (props) => {
  const host = "http://localhost:5000";
  const initialNotes = [];
  const [notes, setNotes] = useState(initialNotes);

  // Get all Notes
  const getNotes = async () => {
    const response = await fetch(`${host}/api/notes/fetchallnotes`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
    });
    const json = await response.json();
    console.log(json);
    setNotes(json);
  };

  // Add a Note
  const addNote = async (title, description, tag) => {
    const note = {
      title: title,
      description: description,
      tag: tag,
    };
    const response = await fetch(`${host}/api/notes/addnote`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
      body: JSON.stringify(note),
    });
    console.log(response);
    setNotes(notes.concat(note));
  };

  // Delete a Note
  const deleteNote = async (id) => {
    const response = await fetch(`${host}/api/notes/deletenote/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
    });
    console.log(response);

    const newNotes = notes.filter((note) => {
      console.log("Deleting the id = " + id);
      return note._id !== id;
    });
    setNotes(newNotes);
  };

  // Edit a Note
  const editNote = async (id, title, description, tag) => {
    const response = await fetch(`${host}/api/notes/updatenote/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
      body: JSON.stringify({ title, description, tag }),
    });
    console.log(response);

    for (let index = 0; index < notes.length; index++) {
      const element = notes[index];
      if (element._id === id) {
        element.title = title;
        element.description = description;
        element.tag = tag;
      }
    }
  };

  return <NoteContext.Provider value={{ notes, addNote, deleteNote, editNote, getNotes }}>{props.children}</NoteContext.Provider>;
};

export default NoteState;
