import React from "react";

// const ChangeName = (props) => {
// const ChangeName = ({ setUsername }) => {
const ChangeName = ({ username, setUsername }) => {
    const handlePropChnage = () => {
        // function to change the name
        // props.changeName("there");
        setUsername("there");
    };
    return (
        <div>
            <button onClick={handlePropChnage}>Hide my Name</button>
            <p>{username}, what do you have planned for today </p>
        </div>
    );
};

export default ChangeName;
