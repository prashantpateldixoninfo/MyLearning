import './App.css';
import { React, useState } from 'react';

function App() {
  // let name = "Prashant";
  const [name, setName] = useState("Prashant");
  const [flag, setFlag] = useState(false);
  const [steps, setSteps] = useState(0);
  const [names, setNames] = useState([]);

  function changeName() {
    console.log("I clicked !!!");
    setName("Patel");
    setFlag(!flag);
  }

  function increment() {
    setSteps((e) => e + 1);
    setSteps((e) => e + 1);
  }

  function decrement() {
    setSteps(steps - 1);
  }

  function addNames(e) {
    e.preventDefault(); // To stop the page refresh
    setNames([...names, { id: names.length, name: name }]);
    console.log("names => ", names);
  }

  return (
    <div className="App">
      <h1>Hello {flag ? name : "???"}</h1>
      <button onClick={changeName}>Click Me</button>
      <hr></hr>
      <button onClick={increment}>+</button>
      <h2>{steps}</h2>
      <button onClick={decrement}>-</button>
      <hr></hr>
      <form onSubmit={addNames}>
        <input
          type="text"
          name="name"
          placeholder='add names'
          onChange={(e) => setName(e.target.value)}>
        </input>
        <button>Submitt</button>
      </form>
      <hr></hr>
      <ul>
        {names.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}


export default App;
