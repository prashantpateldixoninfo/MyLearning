import './App.css';
import { useEffect, useRef, useState } from "react";

/* DOM Reference */
/* useRef for storing previous state/value */

function App() {

  const [name, setName] = useState();
  const [counter, setCounter] = useState(Math.ceil(Math.random() * 100));
  let inputRef = useRef(null);
  let previousRandNum = useRef();
  const firstCatRef = useRef(null);
  const secondCatRef = useRef(null);
  const thirdCatRef = useRef(null);

  function resetInput() {
    setName("");
    inputRef.current.focus();
  }

  useEffect(() => {
    previousRandNum.current = counter;
  }, [counter]);

  function handleScrollToFirstCat() {
    firstCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

  function handleScrollToSecondCat() {
    secondCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

  function handleScrollToThirdCat() {
    thirdCatRef.current.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
      inline: 'center'
    });
  }

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
      <>
        <nav>
          <button onClick={handleScrollToFirstCat}>Tom</button>
          <button onClick={handleScrollToSecondCat}>Maru</button>
          <button onClick={handleScrollToThirdCat}>Jellylorum</button>
        </nav>
        <div>
          <ul>
            <li>
              <img
                src="https://placekitten.com/g/200/200"
                alt="Tom"
                ref={firstCatRef}
              />
            </li>
            <li>
              <img
                src="https://placekitten.com/g/300/200"
                alt="Maru"
                ref={secondCatRef}
              />
            </li>
            <li>
              <img
                src="https://placekitten.com/g/250/200"
                alt="Jellylorum"
                ref={thirdCatRef}
              />
            </li>
          </ul>
        </div>
      </>
      <hr></hr>
    </div>
  );
}

export default App;
