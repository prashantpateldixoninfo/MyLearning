import './App.css';
import { useEffect, useRef, useState } from "react";

/* DOM Reference */
/* useRef for storing previous state/value */

function App() {

  const [name, setName] = useState();
  const [counter, setCounter] = useState(Math.ceil(Math.random() * 100));
  let inputRef = useRef(null);
  let previousRandNum = useRef();

  function resetInput() {
    setName("");
    inputRef.current.focus();
  }

  useEffect(() => {
    previousRandNum.current = counter;
  }, [counter]);

  return (
    <div className="App">
      <hr></hr>
      <input
        ref={inputRef}
        type="text"
        name="name"
        // autoComplete="off"
        value={name}
        onChange={(e) => setName(e.target.value)}>
      </input>
      <button onClick={resetInput}>Reset</button>
      <hr></hr>
      <h1>Random Counter : {counter}</h1>
      { 
        typeof previousRandNum.current !== "undefined" && 
        <h2>Previous Random Num: {previousRandNum.current}</h2>
      }
      <button onClick={() => setCounter(Math.ceil(Math.random() * 100))}>Random Generator</button>
      <hr></hr>
    </div>
  );
}

export default App;
