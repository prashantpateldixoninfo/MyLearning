import React from "react";
import { Link, useNavigate } from "react-router-dom";

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
            // Save the auth token in local storage and redirect to home page
            localStorage.setItem("auth-token", json.authToken);
            if (json.user_type === "buyer") {
                navigate("/buyer");
            } else {
                navigate("/seller");
            }
            props.showAlert("Logged In Successfully", "success");
        } else {
            props.showAlert("Invalid Details : " + json.error, "warning");
        }
    };

    return (
        <div>
            <div className="container d-flex justify-content-center align-items-center my-2">
                <form className="p-1 bg-white rounded shadow border border-2 border-info" style={{ width: "500px" }} onSubmit={handleSubmit}>
                    <h2 className="text-center text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3">vCart Login</h2>
                    <div className="mb-3">
                        <label htmlFor="email" className="form-label">
                            <b style={{ color: "blue" }}>Email address</b>
                        </label>
                        <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" required />
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password" className="form-label">
                            <b style={{ color: "blue" }}>Password</b>
                        </label>
                        <input type="password" className="form-control" id="password" name="password" minLength={5} required />
                    </div>
                    <button type="submit" className="btn btn-primary btn3d d-grid mx-auto mb-2">
                        Login
                    </button>
                </form>
            </div>
            <div container d-flex justify-content-center align-items-center className="my-2">
                <Link className="btn btn-primary d-grid mx-auto" style={{ width: "500px" }} to="/signup" role="button">
                    <span>New User Registration</span>
                </Link>
            </div>
        </div>
    );
};

export default Login;
