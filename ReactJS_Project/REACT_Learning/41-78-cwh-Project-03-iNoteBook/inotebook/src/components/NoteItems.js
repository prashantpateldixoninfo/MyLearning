import React from "react";

const NoteItems = (props) => {
  const { note } = props;
  return (
    <div className="col-md-3">
      <div className="card my-3">
        <div className="card-body">
          <h5 className="card-title">{note.title}</h5>
          <p className="card-text">
            {note.description} Lorem ipsum dolor sit amet consectetur adipisicing elit. Unde placeat doloremque voluptatem vel? Qui earum nemo repudiandae natus? Nobis eos veritatis obcaecati iure
            dolor, dolorum nostrum ea, minus cumque atque quasi. Expedita!
          </p>
        </div>
      </div>
    </div>
  );
};

export default NoteItems;
