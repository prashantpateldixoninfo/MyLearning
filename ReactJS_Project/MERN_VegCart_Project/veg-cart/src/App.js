import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import NavBar from "./components/NavBar";
import Signup from "./components/Signup";

function App() {
    return (
        <div>
            <BrowserRouter>
                <NavBar />
                <div className="container">
                    <Routes>
                        <Route exact path="/" element={<Home key="home" />} />
                        <Route exact path="/home" element={<Home key="home" />} />
                        <Route exact path="/signup" element={<Signup key="signup" />} />
                    </Routes>
                </div>
            </BrowserRouter>
        </div>
    );
}

export default App;
