const username = document.getElementById("username");
const display = document.getElementById("display");

const handleInput = (e) => {
    display.innerHTML = e.target.value;
};

username.addEventListener("input", handleInput);
