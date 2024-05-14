import React, { useState } from "react";
import { useDrop } from "react-dnd";
import { PetCard } from "./PetCard";

const PETS = [
    { id: 1, name: "dog" },
    { id: 2, name: "cat" },
    { id: 3, name: "fish" },
    { id: 4, name: "hamster" },
];

export const Basket = () => {
    const [basket, setBasket] = useState([]);
    const [{ isOver }, dropRef] = useDrop({
        accept: "pet",
        drop: (item) => setBasket((basket) => (!basket.includes(item) ? [...basket, item] : basket)),
        collect: (monitor) => ({
            isOver: monitor.isOver(),
        }),
    });

    return (
        <React.Fragment>
            <div className="pets">
                {PETS.map((pet) => (
                    <PetCard draggable id={pet.id} name={pet.name} />
                ))}
            </div>
            <div className="basket" ref={dropRef}>
                {basket.map((pet) => (
                    <PetCard id={pet.id} name={pet.name} />
                ))}
                {isOver && <div>Drop Here!</div>}
            </div>
        </React.Fragment>
    );
};
