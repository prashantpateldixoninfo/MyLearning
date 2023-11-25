import React, { Component } from "react";

export class Spinner extends Component {
  render() {
    return (
      <div className="text-center">
        <img className="my-3" src={require("./../images/loading.gif")} alt="loading" />
      </div>
    );
  }
}

export default Spinner;
