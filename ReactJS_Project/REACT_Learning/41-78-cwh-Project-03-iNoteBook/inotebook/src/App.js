import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import About from "./components/About";
import Login from "./components/Login";
import Signup from "./components/Signup";
import NoteState from "./context/notes/NoteState";
import Alert from "./components/Alert";

function App() {
  return (
    <div>
      <NoteState>
        <BrowserRouter>
          <NavBar />
          <Alert message="This is amazing React course" />
          <div className="container">
            <Routes>
              <Route exact path="/" element={<Home key="inotebook" />} />
              <Route exact path="/home" element={<Home key="home" />} />
              <Route exact path="/about" element={<About key="about" />} />
              <Route exact path="/login" element={<Login key="login" />} />
              <Route exact path="/signup" element={<Signup key="signup" />} />
            </Routes>
          </div>
        </BrowserRouter>
      </NoteState>
    </div>
  );
}

export default App;
