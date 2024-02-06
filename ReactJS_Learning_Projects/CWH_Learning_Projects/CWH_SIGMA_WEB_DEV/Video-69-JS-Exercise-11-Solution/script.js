let a = prompt("Enter the Number");

function factFor(num) {
    if (num < 0) {
        return `Invalid Number, n must be > or = to 0`;
    }
    let fac = 1;
    for (let index = 1; index <= num; index++) {
        fac = fac * index;
    }
    return fac;
}

function FactRecursive(num) {
    if (num < 0) {
        return `Invalid Number, n must be > or = to 0`;
    }
    if (num == 1 || num == 0) {
        return 1;
    }
    return num * FactRecursive(num - 1);
}

function FactReduce(num) {
    if (num < 0) {
        return `Invalid Number, n must be > or = to 0`;
    }
    let arr = new Array();
    for (i = 1; i <= num; i++) {
        arr.push(i);
    }
    let c = arr.slice(1).reduce((a, b) => a * b);
    return c;
}

alert(`Factorial of(using For Loop) ${`${a}`} is [${`${factFor(a)}`}]`);
alert(`Factorial of(using Recursion) ${`${a}`} is [${`${FactRecursive(a)}`}]`);
alert(`Factorial of(using Reduce) ${`${a}`} is [${`${FactReduce(a)}`}]`);
