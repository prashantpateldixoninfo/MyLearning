import React, { useContext } from "react";
import NoteContext from "../context/notes/NoteContext";
import NoteItems from "./NoteItems";

export default function Notes() {
  const context = useContext(NoteContext);
  const { notes, setNotes } = context;
  return (
    <div className="row my-3">
      <h2>Your's Notes</h2>
      {notes.map((note) => {
        return <NoteItems key={note._id} note={note} />;
      })}
    </div>
  );
}
