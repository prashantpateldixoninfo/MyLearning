import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import About from "./components/About";
import Login from "./components/Login";
import Signup from "./components/Signup";
import NoteState from "./context/notes/noteState";
import Alert from "./components/Alert";
import React, { useState } from "react";

function App() {
  const [alert, setAlert] = useState(null);

  const showAlert = (message, type) => {
    setAlert({
      msg: message,
      type: type,
    });
    setTimeout(() => {
      setAlert(null);
    }, 3000);
  };

  return (
    <div>
      <NoteState>
        <BrowserRouter>
          <NavBar />
          <Alert alert={alert} />
          <div className="container">
            <Routes>
              <Route exact path="/" element={<Home showAlert={showAlert} key="inotebook" />} />
              <Route exact path="/home" element={<Home showAlert={showAlert} key="home" />} />
              <Route exact path="/about" element={<About key="about" />} />
              <Route exact path="/login" element={<Login showAlert={showAlert} key="login" />} />
              <Route exact path="/signup" element={<Signup showAlert={showAlert} key="signup" />} />
            </Routes>
          </div>
        </BrowserRouter>
      </NoteState>
    </div>
  );
}

export default App;
