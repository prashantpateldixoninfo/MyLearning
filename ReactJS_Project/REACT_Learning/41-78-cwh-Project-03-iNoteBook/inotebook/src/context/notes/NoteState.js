import React, { useState } from "react";
import NoteContext from "./NoteContext";

const NoteState = (props) => {
  const host = "http://localhost:5000";
  const initialNotes = [];
  const [notes, setNotes] = useState(initialNotes);

  // Add a Note
  const getNotes = async () => {
    // TODO: API Call
    const response = await fetch(`${host}/api/notes/fetchallnotes`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
    });
    const json = await response.json();
    console.log(json)
  };

  // Add a Note
  const addNote = async (title, description, tag) => {
    // TODO: API Call
    const response = await fetch(`${host}/api/notes/addnote`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
      body: JSON.stringify({
        title: title,
        description: description,
        tag: tag,
      }),
    });
    console.log(response);

    const note = {
      _id: "656839f0794dd73cd9805239",
      user: "6565b77b79761e651113ab51",
      title: title,
      description: description,
      tag: tag,
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    };
    setNotes(notes.concat(note));
  };

  // Delete a Note
  const deleteNote = (id) => {
    // TODO: API Call
    const newNotes = notes.filter((note) => {
      return note._id !== id;
    });
    setNotes(newNotes);
  };

  // Edit a Note
  const editNote = async (id, title, description, tag) => {
    // TODO: API Call
    const response = await fetch(`${host}/api/notes/updatenote/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "auth-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiNjU2NWI3N2I3OTc2MWU2NTExMTNhYjUxIn0sImlhdCI6MTcwMTE3MzUyNn0.v2c2WR7XGXMWC_894ct4e3ogXJeRZjfBlYgLKk8sDFM",
      },
      body: JSON.stringify({title, description, tag}),
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
