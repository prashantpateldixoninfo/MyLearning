import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import About from "./components/About";

function App() {
  return (
    <div>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route exact path="/" element={<Home key="inotebook" />} />
          <Route exact path="/home" element={<Home key="home" />} />
          <Route exact path="/about" element={<About key="about" />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
