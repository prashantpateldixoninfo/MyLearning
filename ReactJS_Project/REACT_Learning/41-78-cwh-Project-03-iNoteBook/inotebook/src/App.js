import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import About from "./components/About";
import NoteState from "./context/notes/NoteState";

function App() {
  return (
    <div>
      <NoteState>
        <BrowserRouter>
          <NavBar />
          <div className="container">
            <Routes>
              <Route exact path="/" element={<Home key="inotebook" />} />
              <Route exact path="/home" element={<Home key="home" />} />
              <Route exact path="/about" element={<About key="about" />} />
            </Routes>
          </div>
        </BrowserRouter>
      </NoteState>
    </div>
  );
}

export default App;
