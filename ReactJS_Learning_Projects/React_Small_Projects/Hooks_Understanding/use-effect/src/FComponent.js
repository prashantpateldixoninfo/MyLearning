import React, { useEffect, useState } from "react";

function FComponent() {

    const [message, setMessage] = useState("Function Component");
    const [time, setTime] = useState(new Date().toString());

    function showDate() {
        setTime(new Date().toString());
    }

    useEffect(() => {
        // Initialization
        const interval = setInterval(showDate, 1000);

        // Cleanup
        return () => {
            clearInterval(interval);
        }
    }, [time, message]/*Dependency*/);

    function changeMessage() {
        setMessage("I am Dixon boy " + Math.floor((Math.random() * 100) + 1)); // 1 to 100 range
    }

    return (
        <div>
            <h1>I am in Function Component</h1>
            <button onClick={changeMessage}>Change Message</button>
            <button onClick={showDate}>Show Date</button>
            <h2>{message}</h2>
            <div>{time}</div>
        </div>
    );
}

export default FComponent;