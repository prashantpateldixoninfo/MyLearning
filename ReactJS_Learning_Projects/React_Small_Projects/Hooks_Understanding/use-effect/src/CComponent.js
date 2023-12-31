import React from "react";

class CComponent extends React.Component {

    state = {
        message: "Class Component",
        time: new Date().toString(),
    }

    componentDidMount() {
        this.interval = setInterval(this.showDate, 1000);
        console.log("I am from Did Mount => ", this.interval);
    }

    componentDidUpdate() {
        console.log("I am from Update => ", this.interval);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
        console.log("I am from Unmount => ", this.interval);
    }

    showDate = () => {
        this.setState({time: new Date().toString()});
    }

    render() {
        return (
            <div>
                <h1>I am in Class Component</h1>
                <h2>{this.state.message}</h2>
                <div>{this.state.time}</div>
            </div>
        );
    }
}

export default CComponent;