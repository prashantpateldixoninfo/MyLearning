import React, { useEffect, useState } from "react";
import { v4 as uuid } from "uuid";
import "./App.css";
import Header from "./Header";
import AddContact from "./AddContact";
import ContactList from "./ContactList";

// const contactlist = [
//   {
//     id: "1",
//     name: "Prashant",
//     email: "pp@gmail.cpm"
//   },
//   {
//     id: 2,
//     name: "Patel",
//     email: "ps@dixon.com"
//   }
// ]

function App() {

  const LOCAL_STORAGE_KEY = "PrashantContacts";
  const [contacts, setContacts] = useState([]);

  const addContactHandler = (c) => {
    console.log("contacts => ", c);
    setContacts([...contacts, {id: uuid(), ...c}]);
  }

  useEffect(() => {
    const retriveContacts = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    if (retriveContacts.length) {
      setContacts(retriveContacts);
    }
  }, []); // [] is called once when page is refreshed

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(contacts));
  }, [contacts]); // It will called when "contancts" get updated

  const removeContactHandler = (id) => {
    console.log("removeContactHandler id => ", id);
    const newContactList = contacts.filter((c) => {
      return c.id !== id;
    })
    setContacts(newContactList);
  }


  return (
    <div className="ui container">
      <Header />
      <AddContact myAddContactHandler={addContactHandler} />
      <ContactList mycontacts={contacts} getContactId={removeContactHandler}/>
    </div>
  );
}

export default App;
