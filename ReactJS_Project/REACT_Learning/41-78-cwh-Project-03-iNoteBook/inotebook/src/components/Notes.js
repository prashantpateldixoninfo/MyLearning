import React, { useState, useContext, useEffect, useRef } from "react";
import NoteContext from "../context/notes/NoteContext";
import NoteItems from "./NoteItems";
import AddNote from "./AddNote";

export default function Notes() {
  const context = useContext(NoteContext);
  const { notes, getNotes } = context;

  useEffect(() => {
    getNotes();
    // eslint-disable-next-line
  }, []);

  const ref = useRef(null);

  const updateNote = (currentNote) => {
    console.log(note);
    ref.current.click();
    setNote({ etitle: currentNote.title, edescription: currentNote.description, etag: currentNote.tag });
  };

  const [note, setNote] = useState({ etitle: "", edescription: "", etag: "" });

  const handleSubmitt = (e) => {
    e.preventDefault();
    // updateNote(note.title, note.description, note.tag);
  };
  const handleChange = (e) => {
    setNote({ ...note, [e.target.name]: e.target.value });
  };

  return (
    <>
      <AddNote />

      <button ref={ref} type="button" className="btn btn-primary d-none" data-bs-toggle="modal" data-bs-target="#exampleModal">
        Launch demo modal
      </button>

      <div className="modal fade" id="exampleModal" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h1 className="modal-title fs-5" id="exampleModalLabel">
                Edit Note
              </h1>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              <form className="my-3">
                <div className="mb-3">
                  <label htmlFor="title" className="form-label">
                    Title
                  </label>
                  <input type="text" className="form-control" id="etitle" name="etitle" value={note.etitle} onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label htmlFor="description" className="form-label">
                    Description
                  </label>
                  <input type="text" className="form-control" id="edescription" name="edescription" value={note.edescription} onChange={handleChange} />
                </div>
                <div className="mb-3">
                  <label htmlFor="tag" className="form-label">
                    Tag
                  </label>
                  <input type="text" className="form-control" id="etag" name="etag" value={note.etag} onChange={handleChange} />
                </div>
              </form>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
              <button type="button" className="btn btn-primary" onSubmit={handleSubmitt}>
                Update Note
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="row my-3">
        <h2>Your's Notes</h2>
        {notes.map((note) => {
          return <NoteItems key={note._id} updateNote={updateNote} note={note} />;
        })}
      </div>
    </>
  );
}
