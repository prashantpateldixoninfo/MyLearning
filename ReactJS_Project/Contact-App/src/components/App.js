import React from "react";
import "./App.css";
import Header from "./Header";
import AddContanct from "./AddContact";
import ContactList from "./ContactList";

function App() {
  const conctacts = [
    {
      id: "1",
      name: "Prashant",
      email: "prashant@gmail.com"
    },
    {
      id: "2",
      name: "test",
      email: "test@gmail.com"
    }
  ];

  return (
    <div className="ui container">
      <Header />
      <AddContanct />
      <ContactList mycontacts={conctacts}/>
    </div>
  );
}

export default App;
