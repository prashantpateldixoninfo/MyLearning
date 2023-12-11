import React, { useState } from "react";
import {useDispatch } from "react-redux";
import { decrement, increment, } from "./counterSlice";
import styles from "./Counter.module.css";

export function Counter() {
  const [incrementAmount, setIncrementAmount] = useState("0");
  const dispatch = useDispatch();

  return (
    <div>
      <div className={styles.row}>
        <button className={styles.button} aria-label="Decrement value" onClick={() => dispatch(decrement(Number(incrementAmount) || 0))}>
          -
        </button>
        <input className={styles.textbox} aria-label="Set increment amount" value={incrementAmount} onChange={(e) => setIncrementAmount(e.target.value)} />
        <button className={styles.button} aria-label="Increment value" onClick={() => dispatch(increment(Number(incrementAmount) || 0))}>
          +
        </button>
      </div>
    </div>
  );
}
