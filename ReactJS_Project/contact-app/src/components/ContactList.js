import React from "react";
import ContactCard from "./ContactCard";

const ContactList = (props) => {
    console.log("mycontact => ", props.mycontacts);
    const renderContactList = props.mycontacts.map((contact) => {
        console.log("contact ==> ", contact);
        return (
            <ContactCard mycontact={contact} />
        );
    });
    return <div className="ui celled list">{renderContactList}</div>
}

// const ContactList = (props) => {
//     console.log("props = >", props);

//     const deleteContactHandler = (id) => {
//         props.getContactId(id);
//     }

//     const renderContactList = props.myContacts.map((contact) => {
//         return (
//             <ContactCard 
//                 myContact={contact}
//                 clickHandler={deleteContactHandler}
//                 key={contact.id}
//             />
//         );
//     })
//     return <div className="ui celled list">{renderContactList}</div>
// }

export default ContactList;