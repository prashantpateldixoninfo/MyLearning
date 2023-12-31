import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import { Counter } from "./redux/action-reducer/Counter";
import Home from "./components/Home";
import About from "./components/About";

function App() {
  return (
    <div>
      <BrowserRouter>
        <NavBar />
        <div className="container">
          <Counter />
        </div>
        <div className="container">
          <Routes>
            <Route exact path="/" element={<Home key="sbp" />} />
            <Route exact path="/home" element={<Home key="home" />} />
            <Route exact path="/about" element={<About key="about" />} />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
