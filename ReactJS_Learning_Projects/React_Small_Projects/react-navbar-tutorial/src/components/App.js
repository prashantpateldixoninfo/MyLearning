import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./Navbar/Navbar";
import Home from "./pages/Home";
import KeyFeatures from "./pages/KeyFeatures";
import Pricing from "./pages/Pricing";
import Testimonials from "./pages/Testimonials";
import Demo from "./pages/Demo";

function App() {
  return (
    <div className='container'>
      <BrowserRouter >
        <Navbar />
        <Routes>
          <Route path="/" Component={Home} />
          <Route path="/features" Component={KeyFeatures} />
          <Route path="/pricing" Component={Pricing} />
          <Route path="/testimonials" Component={Testimonials} />
          <Route path="/demo" Component={Demo} />
        </Routes>
      </BrowserRouter >
    </div>
  );
}

export default App;
