import React, { useEffect, useState } from "react";
import EditTask from "./EditTask";
import { useDrag } from "react-dnd";

const ToDo = ({ task, taskList, setTaskList }) => {
    const [timer, setTimer] = useState(task.duration);
    const [running, setRunning] = useState(false);
    const [{ isDragging }, drag] = useDrag(() => ({
        type: "todo",
        collect: (monitor) => ({
            isDragging: !!monitor.isDragging(),
        }),
    }));

    useEffect(() => {
        let interval;
        if (running) {
            interval = setInterval(() => {
                setTimer((prevTime) => prevTime + 10);
            }, 10);
        } else if (!running) {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [running]);

    const handleStop = () => {
        setRunning(false);
        let taskIndex = taskList.indexOf(task);
        taskList.splice(taskIndex, 1, {
            projectName: task.projectName,
            taskDescription: task.taskDescription,
            timestamp: task.timestamp,
            duration: timer,
        });
        localStorage.setItem("taskList", JSON.stringify(taskList));
        window.location.reload();
    };

    // const handleDelete = (itemID) => {
    //     let removeIndex = taskList.indexOf(task);
    //     taskList.splice(removeIndex, 1);
    //     setTaskList((currentTasks) => currentTasks.filter((todo) => todo.id !== itemID));
    // };

    const handleDeleteTask = () => {
        // let remainingTasks = taskList.filter((t) => t.projectName !== task.projectName || t.taskDescription !== task.taskDescription);
        let removeIndex = taskList.indexOf(task);
        taskList.splice(removeIndex, 1);
        localStorage.setItem("taskList", JSON.stringify(taskList));
        window.location.reload();
    };
    return (
        <>
            <div
                ref={drag}
                className="flex flex-col items-start 
                justify-start bg-purple-300 my-4 ml-6
                py-4 px-6 w-3/4 max-w-lg"
            >
                <div className="w-full flex flex-row justify-between">
                    <p className="font-semi-bold text-xl">{task.projectName}</p>
                    <EditTask task={task} taskList={taskList} setTaskList={setTaskList} />
                </div>
                <p className="text-lg py-2">{task.taskDescription}</p>
                <div className="w-full flex flex-row items-center justify-evenly">
                    <div className="w-1/4 min-w-max text-xl font-semibold py-4">
                        <span>{("0" + Math.floor((timer / 3600000) % 24)).slice(-2)}:</span>
                        <span>{("0" + Math.floor((timer / 60000) % 60)).slice(-2)}:</span>
                        <span>{("0" + Math.floor((timer / 1000) % 60)).slice(-2)}:</span>
                        <span className="text-sm">{("0" + ((timer / 10) % 60)).slice(-2)}</span>
                    </div>
                    <div className="flex flex-row justify-evenly gap-4">
                        {running ? (
                            <button className="border rounded-lg py-1 px-3" onClick={handleStop}>
                                Stop
                            </button>
                        ) : (
                            <button
                                className="border rounded-lg py-1 px-3"
                                onClick={() => {
                                    setRunning(true);
                                }}
                            >
                                Start
                            </button>
                        )}
                        <button className="border rounded-lg py-1 px-3" onClick={() => setTimer(0)}>
                            Reset
                        </button>
                    </div>
                </div>
                <div className="w-full flex justify-center">
                    <button
                        className="bg-red-500 text-white 
                        text-sm uppercase font-semi-bold 
                        py-1.5 mt-6 mb-1 px-3 rounded-lg"
                        onClick={handleDeleteTask}
                    >
                        Delete
                    </button>
                </div>
            </div>
        </>
    );
};

export default ToDo;
