import './App.css';
import { useState } from "react";

function App() {
  const initialValue = {username: "", email: "", password: ""};
  const [formValues, setFormValues] = useState(initialValue);

  // console.log("formValues = ", formValues);

  // const handleChange = () => {
  //   console.log("Prashant Patel");
  // }

  function handleChange(e) {
    // console.log("Prashant Patel => ", e.target);
    const {name, value} =  e.target;
    // console.log("name => ", name);
    // console.log("value => ", value);
    setFormValues({...formValues, [name]: value});
    // console.log("formValues => ", formValues);
  }

  return (
    <div className='container'>
      <form>
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
          <button className='fluid ui button green'>Submit</button>
        </div>
      </form>
    </div>
  );
}

export default App;
