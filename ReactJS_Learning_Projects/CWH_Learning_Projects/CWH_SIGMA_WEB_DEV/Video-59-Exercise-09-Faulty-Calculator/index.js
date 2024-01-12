/* Create a faulty calculator using JavaScript

This faulty calculator does following:
1. It takes two numbers as input from the user
2. It perfoms wrong operations as follows:

+ ---> -
* ---> +
- ---> /
/ ---> **


It performs wrong operation 10% of the times

*/

const readline = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout,
});

readline.question("Enter the values to calculate for +, -, *, & / => like 5+6 without space\n", (cmd) => {
    console.log(`You had Entered => ${cmd}`);

    if (cmd.length === 3) {
        const num = cmd.split("", 3);
        console.log(`Your Result Is : [${clx(parseInt(num[0]), num[1], parseInt(num[2]))}]`);
    } else {
        console.error("!!!ERROR!!! Enter the proper value like => '5+7' without spaces");
    }

    readline.close();
});

function clx(a, op, b) {
    // Returns a random integer from 1 to 100:
    let faultyChance = Math.floor(Math.random() * 100) + 1;

    if (faultyChance < 11) {
        if (op === "+") {
            return a - b;
        } else if (op === "-") {
            return a / b;
        } else if (op === "*") {
            return a + b;
        } else if (op === "/") {
            return a ** b;
        }
    } else {
        if (op === "+") {
            return a + b;
        } else if (op === "-") {
            return a - b;
        } else if (op === "*") {
            return a * b;
        } else if (op === "/") {
            return a / b;
        }
    }
}
