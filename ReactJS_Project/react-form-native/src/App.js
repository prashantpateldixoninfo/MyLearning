import './App.css';
import { useState } from "react";

function App() {
  const initialValue = { username: "", email: "", password: "" };
  const [formValues, setFormValues] = useState(initialValue);
  const [formErrors, setFormErrors] = useState({});

  // console.log("formValues = ", formValues);

  // const handleChange = () => {
  //   console.log("Prashant Patel");
  // }

  function handleChange(e) {
    // console.log("Prashant Patel => ", e.target);
    const { name, value } = e.target;
    // console.log("name => ", name);
    // console.log("value => ", value);
    setFormValues({ ...formValues, [name]: value });
    // console.log("formValues => ", formValues);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // console.log("Submit ==> ", formValues);
    // Validate the formValues
    setFormErrors(validate(formValues));
  }

  function validate(values) {
    const errors = {};
    // console.log("validate ==> ", values);
    const regex_email = /^\S+@\S+\.\S+$/i;

    // Username Validation
    if (values.username === "") { // Emptyness
      errors.username = "Username is required";
      // console.log(errors.username);
    }

    // Email Validation
    if (values.email === "") { // Emptyness
      errors.email = "Email is required";
      // console.log(errors.email);
    }
    else if (!regex_email.test(values.email)) {
      errors.email = "Email format is not valid";
    }


    // Password Validation
    if (values.password === "") { // Emptyness
      errors.password = "Password is required";
      // console.log(errors.password);
    }
    else if (values.password.length < 4 || values.password.length > 10) {
      errors.password = "Password length should be between 4 and 10";
    }

    return errors;
  }

  return (
    <div className='container'>
      <pre>{JSON.stringify(formValues, undefined, 2)}</pre>
      <form onSubmit={handleSubmit}>
        <h1>Login Form</h1>
        <div className='ui divider'></div>
        <div className='ui form'>
          <div className='field'>
            <label>Username</label>
            <input
              type="text"
              name="username"
              placeholder='Full Name'
              value={formValues.username}
              onChange={handleChange}
            >
            </input>
          </div>
          <p>{formErrors.username}</p>
          <div className='field'>
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder='Email ID'
              value={formValues.email}
              onChange={handleChange}
            >
            </input>
          </div>
          <p>{formErrors.email}</p>
          <div className='field'>
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder='Your Password'
              value={formValues.password}
              onChange={handleChange}
            >
            </input>
          </div>
          <p>{formErrors.password}</p>
          <button className='fluid ui button green'>Submit</button>
        </div>
      </form>
    </div>
  );
}

export default App;
