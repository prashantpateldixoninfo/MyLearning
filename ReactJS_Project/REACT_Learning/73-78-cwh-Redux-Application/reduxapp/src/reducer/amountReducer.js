export default reducer = (state = 0, action) => {
  if (action === "deposit") {
    return state + action.payload;
  } else if (action === "withdraw") {
    return state - action.payload;
  } else {
    return state;
  }
};
