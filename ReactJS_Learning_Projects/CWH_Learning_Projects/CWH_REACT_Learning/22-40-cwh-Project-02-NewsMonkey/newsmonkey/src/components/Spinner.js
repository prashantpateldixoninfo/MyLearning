import React from "react";

const Spinner = () => {
  return (
    <div className="text-center">
      <img
        className="my-3"
        src={require("./../images/loading.gif")}
        alt="loading"
      />
    </div>
  );
};

export default Spinner;
