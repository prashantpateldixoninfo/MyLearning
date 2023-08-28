import React from "react";

class AddContact extends React.Component {
    render() {
        return (
            <div className="ui main">
                <h2>Add Contact</h2>
                <form className="ui form">
                    <div className="field">
                        <label>Name</label>
                        <input type="text" name="name" placeholder="Write Your Full Name" />
                    </div>
                    <div className="field">
                        <label>Email</label>
                        <input type="text" name="email" placeholder="Write your email" />
                    </div>
                    <button className="ui button primary">Add</button>
                </form>
            </div>
        );
    }
}

export default AddContact;