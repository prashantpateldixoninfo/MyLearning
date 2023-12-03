import React, { useState } from "react";
import NoteContext from "./NoteContext";


const NoteState = (props) => {
  const initialNotes = [
    {
      "_id": "656839f0794dd73cd9805231",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-01",
      "description": "My Description - 01",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805232",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-02",
      "description": "My Description - 02",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805233",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-03",
      "description": "My Description - 03",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805234",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-04",
      "description": "My Description - 04",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805235",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-05",
      "description": "My Description - 05",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805236",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-06",
      "description": "My Description - 06",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    },
    {
      "_id": "656839f0794dd73cd9805237",
      "user": "6565b77b79761e651113ab51",
      "title": "My Title-07",
      "description": "My Description - 07",
      "tag": "personal",
      "date": "2023-11-30T07:29:52.142Z",
      "__v": 0
    }
  ]
  const [notes, setNotes] = useState(initialNotes);
  return <NoteContext.Provider value={{notes, setNotes}}>{props.children}</NoteContext.Provider>;
};

export default NoteState;
