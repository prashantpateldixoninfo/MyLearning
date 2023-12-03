import React, { useState } from "react";
import NoteContext from "./NoteContext";

const NoteState = (props) => {
  const initialNotes = [
    {
      _id: "656839f0794dd73cd9805231",
      user: "6565b77b79761e651113ab51",
      title: "My Title-01",
      description: "My Description - 01",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805232",
      user: "6565b77b79761e651113ab51",
      title: "My Title-02",
      description: "My Description - 02",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805233",
      user: "6565b77b79761e651113ab51",
      title: "My Title-03",
      description: "My Description - 03",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805234",
      user: "6565b77b79761e651113ab51",
      title: "My Title-04",
      description: "My Description - 04",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805235",
      user: "6565b77b79761e651113ab51",
      title: "My Title-05",
      description: "My Description - 05",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805236",
      user: "6565b77b79761e651113ab51",
      title: "My Title-06",
      description: "My Description - 06",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
    {
      _id: "656839f0794dd73cd9805237",
      user: "6565b77b79761e651113ab51",
      title: "My Title-07",
      description: "My Description - 07",
      tag: "personal",
      date: "2023-11-30T07:29:52.142Z",
      __v: 0,
    },
  ];
  const [notes, setNotes] = useState(initialNotes);

  // Add a Note
  const addNote = (title, description, tag) => {
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
    const newNotes = notes.filter((note) => {return note._id !== id})
    setNotes(newNotes);
  };

  // Edit a Note
  const editNote = (id, title, description, tag) => {};

  return <NoteContext.Provider value={{ notes, addNote, deleteNote, editNote }}>{props.children}</NoteContext.Provider>;
};

export default NoteState;
