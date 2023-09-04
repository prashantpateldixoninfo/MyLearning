import './App.css';

function App() {
  return (
    <div className='container'>
      <form>
        <h1>Login Form</h1>
        <div className='ui divider'></div>
        <div className='ui form'>
          <div className='field'>
            <label>Username</label>
            <input type="text" name="username" placeholder='Full Name'>
            </input>
          </div>
          <div className='field'>
            <label>Email</label>
            <input type="email" name="email" placeholder='Email ID'>
            </input>
          </div>
          <div className='field'>
            <label>Password</label>
            <input type="password" name="password" placeholder='Your Password'>
            </input>
          </div>
          <button className='fluid ui button green'>Submit</button>
        </div>
      </form>
    </div>
  );
}

export default App;
