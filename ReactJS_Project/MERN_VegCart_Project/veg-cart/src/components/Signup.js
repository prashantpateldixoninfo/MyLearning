import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const host = "http://localhost:5000";

const Signup = (props) => {
    const navigate = useNavigate();
    const [userTyper, setUserType] = useState("buyer");

    const handleSubmit = async (formInput) => {
        formInput.preventDefault();

        // console.log("handleSubmit =>", formInput);

        if (formInput.target[4].value !== formInput.target[5].value) {
            props.showAlert("Password mismatch !!!", "info");
            return;
        }
        if (formInput.target[1].checked && formInput.target[6].value !== "Dixon#321") {
            props.showAlert("PassCode mismatch !!!", "info");
            return;
        }

        const userInfo = {
            name: formInput.target[2].value,
            email: formInput.target[3].value,
            password: formInput.target[4].value,
            user_type: formInput.target[0].checked ? formInput.target[0].value : formInput.target[1].value,
        };

        console.log("userInfo =>", userInfo);

        const response = await fetch(`${host}/api/auth/createuser`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userInfo),
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

    const handleRadioButtonInput = (radioInput) => {
        setUserType(radioInput.target.value);
        // console.log(radioInput.target.value);
    };

    return (
        <div className="container d-flex justify-content-center align-items-center my-2">
            <form className="p-1 bg-white rounded shadow border border-2 border-info" style={{ width: "500px" }} onSubmit={handleSubmit}>
                <h2 className="text-center text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3">Create vCart Account</h2>
                <div className="mb-3">
                    <label className="form-label form-check-inline" htmlFor="user-buyer user-seller">
                        <b style={{ color: "blue" }}>User Type</b>
                    </label>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="user-type" id="user-buyer" value="buyer" onChange={handleRadioButtonInput} />
                        <label className="form-check-label" htmlFor="user-buyer">
                            Buyer
                        </label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="user-type" id="user-seller" value="seller" onChange={handleRadioButtonInput} />
                        <label className="form-check-label" htmlFor="user-seller">
                            Seller
                        </label>
                    </div>
                </div>
                <div className="mb-3">
                    <label htmlFor="name" className="form-label">
                        <b style={{ color: "blue" }}>Name</b>
                    </label>
                    <input type="text" className="form-control" id="name" name="name" required />
                </div>
                <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                        <b style={{ color: "blue" }}>Email address</b>
                    </label>
                    <input type="email" className="form-control" id="email" name="email" aria-describedby="emailHelp" required />
                    <div id="emailHelp" className="form-text">
                        We'll never share your email with anyone else.
                    </div>
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                        <b style={{ color: "blue" }}>Password</b>
                    </label>
                    <input type="password" className="form-control" id="password" name="password" minLength={5} required />
                </div>
                <div className="mb-3">
                    <label htmlFor="cpassword" className="form-label">
                        <b style={{ color: "blue" }}>Re-Password</b>
                    </label>
                    <input type="password" className="form-control" id="cpassword" name="cpassword" minLength={5} required />
                </div>
                {userTyper === "seller" && (
                    <div className="mb-3">
                        <label htmlFor="passcode" className="form-label">
                            <b style={{ color: "blue" }}>PassCode</b>
                        </label>
                        <input type="password" className="form-control" id="passcode" name="passcode" minLength={5} required />
                    </div>
                )}
                <button type="submit" className="btn btn-magick btn3d d-grid mx-auto mb-2">
                    Create
                </button>
            </form>
        </div>
    );
};

export default Signup;
