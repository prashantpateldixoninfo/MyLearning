// App.js
import React from "react";
import { DndProvider, useDrag, useDrop } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

const ItemTypes = {
    BOX: "box",
};

const Box = ({ name, isDropped, onDrop }) => {
    const [{ isDragging }, drag] = useDrag(() => ({
        type: ItemTypes.BOX,
        item: { name },
        collect: (monitor) => ({
            isDragging: monitor.isDragging(),
        }),
    }));

    const [, drop] = useDrop(() => ({
        accept: ItemTypes.BOX,
        drop: () => onDrop(name),
    }));

    return (
        <div
            ref={(node) => drag(drop(node))}
            style={{
                opacity: isDragging ? 0.5 : 1,
                cursor: "move",
                border: "1px dashed gray",
                backgroundColor: isDropped ? "lightgreen" : "white",
                padding: "0.5rem",
                margin: "0.5rem",
            }}
        >
            {name}
        </div>
    );
};

const Container = () => {
    const [droppedBoxes, setDroppedBoxes] = React.useState([]);

    const handleDrop = (name) => {
        setDroppedBoxes((prevBoxes) => [...prevBoxes, name]);
    };

    return (
        <div>
            <h2>Drag and Drop Example</h2>
            <div style={{ display: "flex" }}>
                <div style={{ flexGrow: 1 }}>
                    <h3>Draggable Items</h3>
                    <Box name="Item 1" isDropped={droppedBoxes.includes("Item 1")} onDrop={handleDrop} />
                    <Box name="Item 2" isDropped={droppedBoxes.includes("Item 2")} onDrop={handleDrop} />
                </div>
                <div style={{ flexGrow: 1 }}>
                    <h3>Dropped Items</h3>
                    {droppedBoxes.map((name, index) => (
                        <div key={index}>{name}</div>
                    ))}
                </div>
            </div>
        </div>
    );
};

const App = () => {
    return (
        <DndProvider backend={HTML5Backend}>
            <Container />
        </DndProvider>
    );
};

export default App;
