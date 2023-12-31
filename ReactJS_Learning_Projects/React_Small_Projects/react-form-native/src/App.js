import './App.css';
import { useEffect, useState } from "react";

function App() {
  const initialValue = { username: "", email: "", password: "" };
  const [formValues, setFormValues] = useState(initialValue);
  const [formErrors, setFormErrors] = useState({});
  const [isSubmit, setIsSubmit] = useState(false);

  // const handleChange = () => {
  //   console.log("Prashant Patel");
  // }

  function handleChange(e) {
    const { name, value } = e.target;
    setFormValues({ ...formValues, [name]: value });
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate the formValues
    setFormErrors(validate(formValues));
    setIsSubmit(true);
  }

  useEffect(() => {
    console.log(formErrors);
    if (Object.keys(formErrors).length === 0 && isSubmit) {
      console.log(formValues);
    }
  }, [formErrors]);

  function validate(values) {
    const errors = {};
    const regex_email = /^\S+@\S+\.\S+$/i;

    // Username Validation
    if (values.username === "") { // Emptyness
      errors.username = "Username is required";
    }

    // Email Validation
    if (values.email === "") { // Emptyness
      errors.email = "Email is required";
    }
    else if (!regex_email.test(values.email)) {
      errors.email = "Email format is not valid";
    }

    // Password Validation
    if (values.password === "") { // Emptyness
      errors.password = "Password is required";
    }
    else if (values.password.length < 4 || values.password.length > 10) {
      errors.password = "Password length should be between 4 and 10";
    }

    return errors;
  }

  return (
    <div className='container'>
      {
        Object.keys(formErrors).length === 0 && isSubmit ?
          (<div
            className='ui message success'
            style={
              {
                color: "green",
                background: "yellow"
              }
            }>Signed in Successfully</div>) :
          (<div>
            <div
              className='ui message success'
              style={
                {
                  color: "red",
                  background: "yellow"
                }
              }>Signed in Failed</div>
            <pre>{JSON.stringify(formValues, undefined, 2)}</pre>
          </div>
          )
      }
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
