import React, { Component } from "react";

export class Spinner extends Component {
  render() {
    return (
      <div className="text-center">
        <img src={require("./../images/loading.gif")} alt="loading" />
      </div>
    );
  }
}

export default Spinner;
