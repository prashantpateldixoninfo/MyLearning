import React from "react";
import { useNavigate } from "react-router-dom";

const host = "http://localhost:5000";

const Signup = (props) => {
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (e.target[2].value !== e.target[3].value) {
      props.showAlert("Password mismatch !!!", "info");
      return;
    }
    const user = {
      name: e.target[0].value,
      email: e.target[1].value,
      password: e.target[2].value,
    };

    const response = await fetch(`${host}/api/auth/createuser`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    });
    const json = await response.json();

    if (json.success) {
      props.showAlert("Account Created Successfully", "success");
      // Redirect to home page
      navigate("/");
    } else {
      props.showAlert("Invalid Credential : " + json.error, "warning");
    }
  };

  return (
    <div className="mt-2">
      <h2 className="my-3 p-2 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3" style={{width: "30rem"}}><u>Create an account in iNoteBook</u></h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="name" className="form-label">
            Name
          </label>
          <input type="text" className="form-control" id="name" name="name" required />
        </div>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">
            Email address
          </label>
          <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" required />
          <div id="emailHelp" className="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input type="password" className="form-control" id="password" name="password" minLength={5} required />
        </div>
        <div className="mb-3">
          <label htmlFor="cpassword" className="form-label">
            Password
          </label>
          <input type="password" className="form-control" id="cpassword" name="cpassword" minLength={5} required />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
};

export default Signup;
