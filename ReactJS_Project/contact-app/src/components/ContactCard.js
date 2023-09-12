import React from "react";
import avatar from "../images/avatar.jpg";


const ContactCard = (props) => {
    const { id, name, email } = props.mycontact;
    const url = "https://source.unsplash.com/1600x900/?nature,water"
    return (
        <div className="item">
            <div className="content">
                <div className="header">{id}.</div>
                <img className="ui avatar image" src={avatar} alt="NO" />
                <div className="header">{name}</div>
                <img className="ui avatar image" src={url} alt="NO" />
                <div>{email}</div>
            </div>
            <i className="trash alternate outline icon"
                style={
                    {
                        color: "green",
                        float: "right",
                        padding: "0px, 40px"
                    }
                }>
            </i>
        </div>
    );
}
// const ContactCard = (props) => {
//   const { id, name, email } = props.myContact;
//   console.log("My Contact => ", props.myContact);
//   return (
//     <div className="item">
//       <img className="ui avatar image" src={avatar} alt="avatar" />
//       <div className="container">
//         <div className="header" >{name}</div>
//         <div>{email}</div>
//         <i
//           className="trash alternate outline icon"
//           style={
//             {
//               color: "green",
//               // marginLeft: "20px",
//               // paddingLeft: "20px",
//               float: "right"
//             }
//           }
//           onClick={() => props.clickHandler(id)}
//         ></i>
//       </div>
//     </div>
//   );
// };

export default ContactCard;