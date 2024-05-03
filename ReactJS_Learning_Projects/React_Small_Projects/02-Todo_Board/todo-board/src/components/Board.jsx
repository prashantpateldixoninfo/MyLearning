import React from 'react'
import { useState} from 'react';

const Board = ({ task, index, taskList, setTaskList}) => {

  const handleDeleteTask = () => {
    let removeIndex = taskList.indexOf(task);
    taskList.splice(removeIndex, 1);
    setTaskList((currentTasks => currentTasks.filter(todo => index === removeIndex)));
  }
  const [date, setDate] = useState(new Date());
  
  return (
    <div className="max-w-md rounded-xl flex flex-col items-center justify-start border
    text-center text-lg pt-3 pb-4 px-4 md:px-6">
      <p>{task}</p>
      <p>Created: {date.toLocaleTimeString()}</p>
      <button
        className="bg-red-500 texgt-white rounded-lg py-1 px-2"
      onClick={handleDeleteTask}>Delete</button>
    </div>
  )
}

export default Board
