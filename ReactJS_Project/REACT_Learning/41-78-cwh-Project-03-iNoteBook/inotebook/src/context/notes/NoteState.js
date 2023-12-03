import React, { useState } from "react";
import NoteContext from "./NoteContext";


const NoteState = (props) => {
  const initialNotes = [
    {
      "_id": "656839f0794dd73cd9805232",
      "user": "6565b77b79761e651113ab51",
      "title": "cloudNote1 update",
      "description": "My first Note1 update",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805232",
      "user": "6565b77b79761e651113ab51",
      "title": "cloudNote1 update2",
      "description": "My first Note1 update",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    }
  ]
  const [notes, setNotes] = useState(initialNotes);
  return <NoteContext.Provider value={{notes, setNotes}}>{props.children}</NoteContext.Provider>;
};

export default NoteState;
