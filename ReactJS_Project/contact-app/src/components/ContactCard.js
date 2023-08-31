import React from "react";
import avatar from "../images/avatar.jpg";

const ContactCard = (props) => {
    const { id, name, email } = props.myContact;
    console.log("My Contact => ", props.myContact);
    return (
      <div className="item">
        <img className="ui avatar image" src={avatar} alt="avatar" />
        <div className="content">
          <div className="header">{name}</div>
          <div>{email}</div>
        </div>
        <i
          className="trash alternate outline icon"
          style={{ color: "red", marginTop: "7px" }}
          onClick={() => props.clickHandler(id)}
        ></i>
      </div>
    );
  };

export default ContactCard;