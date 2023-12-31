import React from "react";
import { useNavigate } from "react-router-dom";

const host = "http://localhost:5000";

const Login = (props) => {
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const auth = {
      email: e.target[0].value,
      password: e.target[1].value,
    };

    const response = await fetch(`${host}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(auth),
    });
    const json = await response.json();

    if (json.success) {
      // Save the auth token and redirect
      localStorage.setItem("auth-token", json.authToken);
      navigate("/");
      props.showAlert("Logged In Successfully", "success");
    } else {
      props.showAlert("Invalid Details : " + json.error, "warning");
    }
  };

  return (  
    <div className="mt-2">
      <h2 className="my-3 p-3 text-success-emphasis bg-success-subtle border border-success-subtle rounded-3" style={{width: "20rem"}}><u>Login to iNoteBook</u></h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email address
          </label>
          <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" />
          <div id="emailHelp" className="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input type="password" className="form-control" id="password" name="password" />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

export default Login;
