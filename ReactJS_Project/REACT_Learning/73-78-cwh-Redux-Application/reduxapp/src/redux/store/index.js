import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "../action-reducer/counterSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
});
