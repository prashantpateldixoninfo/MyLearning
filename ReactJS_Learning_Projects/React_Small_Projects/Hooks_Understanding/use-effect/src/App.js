import './App.css';
import CComponent from "./CComponent";
import FComponent from "./FComponent";
import React, { useState } from "react";

function App() {

  const [cflag, setCflag] = useState(true);

  // const toggleButton = () => {
  //   setCflag(!cflag);
  // }

  return (
    <div className="App">
      <hr></hr>
      <h1>Hello, This is App Component</h1>
      <button onClick={() => setCflag(!cflag)}>Toggle The Component</button>
      <hr></hr>
      {cflag ? <CComponent /> : <FComponent />}
      <hr></hr>
    </div>
  );
}

export default App;
