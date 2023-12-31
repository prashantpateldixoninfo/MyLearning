import "./App.css";
import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import NavBar from "./components/NavBar";
import Signup from "./components/Signup";
import Login from "./components/Login";
import Alert from "./components/Alert";
import Buyer from "./components/Buyer";
import Seller from "./components/Seller";

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
            <BrowserRouter>
                <NavBar />
                <Alert alert={alert} />
                <div className="container">
                    <Routes>
                        <Route exact path="/" element={<Home key="home" />} />
                        <Route exact path="/home" element={<Home key="home" />} />
                        <Route exact path="/buyer" element={<Buyer key="buyer" />} />
                        <Route exact path="/seller" element={<Seller key="seller" />} />
                        <Route exact path="/signup" element={<Signup showAlert={showAlert} key="signup" />} />
                        <Route exact path="/login" element={<Login showAlert={showAlert} key="login" />} />
                    </Routes>
                </div>
            </BrowserRouter>
        </div>
    );
}

export default App;
