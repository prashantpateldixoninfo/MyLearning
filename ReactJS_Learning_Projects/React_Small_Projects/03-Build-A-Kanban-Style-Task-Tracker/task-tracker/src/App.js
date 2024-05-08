import { useEffect, useState } from "react";
import AddTask from "./components/AddTask";
import ToDo from "./components/ToDo";

function App() {
    const [taskList, setTaskList] = useState([]);

    useEffect(() => {
        let tasklist = localStorage.getItem("taskList");
        if (tasklist) {
            setTaskList(JSON.parse(tasklist));
        }
    }, []);

    return (
        <>
            <h1 className="text-2xl font-bold py-4 pl-6">The Task Tracker</h1>
            <p className="text-xl pl-6">Hi There!</p>
            <div className="flex flex-row items-center">
                <p className="text-xl pl-6">Click</p>
                <AddTask taskList={taskList} setTaskList={setTaskList} />
                <p className="text-xl my-2">to add a new task</p>
            </div>
            <div>
                <h2
                    className="bg-orange-300 text-xl font-semi-bold 
                    ml-6 my-4 px-4 py-2  w-3/4 max-w-lg"
                >
                    To Do:
                </h2>
                {taskList.map((task, i) => (
                    <ToDo key={i} task={task} taskList={taskList} setTaskList={setTaskList} />
                ))}
            </div>
        </>
    );
}

export default App;
