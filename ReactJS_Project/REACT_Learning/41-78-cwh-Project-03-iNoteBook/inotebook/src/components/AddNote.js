import React, { useContext, useState } from "react";
import NoteContext from "../context/notes/NoteContext";

const AddNote = () => {
  const context = useContext(NoteContext);
  const { addNote } = context;

  const [note, setNote] = useState({ title: "", description: "", tag: "default" });
  const handleSubmitt = (e) => {
    e.preventDefault();
    addNote(note.title, note.description, note.tag);
  };

  const handleChange = (e) => {
    setNote({ ...note, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <div className="container my-3">
        <h2>Add a Note</h2>
        <form className="my-3">
          <div className="mb-3">
            <label htmlFor="title" className="form-label">
              Title
            </label>
            <input type="text" className="form-control" id="title" name="title" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label htmlFor="description" className="form-label">
              Description
            </label>
            <input type="text" className="form-control" id="description" name="description" onChange={handleChange} />
          </div>
          <div className="mb-3">
            <label htmlFor="tag" className="form-label">
              Tag
            </label>
            <input type="text" className="form-control" id="tag" name="tag" onChange={handleChange} />
          </div>
          <div className="my-3 mb-3">
            <button type="submit" className="btn btn-primary" onClick={handleSubmitt}>
              Add Note
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddNote;
