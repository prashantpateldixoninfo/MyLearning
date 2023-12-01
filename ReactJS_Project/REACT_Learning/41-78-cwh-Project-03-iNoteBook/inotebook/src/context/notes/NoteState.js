import React from "react";
import NoteContext from "./NoteContext";
import { useState } from "react";

const NoteState = (props) => {
  const s1 = {
    name: "Prashant",
    class: "11B",
  };
  const [state, setState] = useState(s1);
  const update = () => {
    setTimeout(() => {
      setState({ name: "Naman", class: "8C" });
    }, 5000);
  };
  return <NoteContext.Provider value={{state, update}}>{props.children}</NoteContext.Provider>;
};

export default NoteState;
