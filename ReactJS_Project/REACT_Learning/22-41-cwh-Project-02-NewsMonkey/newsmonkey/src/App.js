import "./App.css";

import React, { Component } from "react";
import NavBar from "./components/NavBar";
import News from "./components/News";

export default class App extends Component {
  c = "John";
  render() {
    return (
      <div>
        <NavBar />
        <News pageSize={15}/>
      </div>
    );
  }
}
