import "./App.css";
import { useState } from "react";
import ChangeName from "./ChangeName";

function App() {
    const [username, setUsername] = useState("");
    const handleInput = (e) => {
        setUsername(e.target.value);
    };
    return (
        <div>
            <h1>04 - State and Props</h1>
            <label htmlFor="username">Enter Your Name: </label>
            <input id="username" type="text" placeholder="Your wonderful name" onChange={handleInput} />
            <p>Hi there, {username}</p>
            <p>{username}, you are doing great today</p>
            {/* <ChangeName changeName={(uname) => setUsername(uname)} />  Bad way, Not recommended  */}
            {/* <ChangeName setUsername={setUsername} /> */}
            <ChangeName username={username} setUsername={setUsername} />
        </div>
    );
}

export default App;
