// Write a program to calculate factorial of a number using reduce and using for loops

// 6! = 6*5*4*3*2*1

let a = prompt("Enter the Number");

function factorial(num) {
    if (num < 0) {
        return `Invalid Number, n must be > or = to 0`;
    }
    if (num == 1 || num == 0) {
        return 1;
    }
    return num * factorial(num - 1);
}

function factor(num) {
    var data = new Array();
    for (i = 1; i <= num; i++) {
        data.push(i);
    }
    return data.reduce(function (a, b) {
        return a * b;
    }, 1);
}

alert(`The result is(recursive) ${`${factorial(a)}`}`);
alert(`The result is(using reduce) ${`${factor(a)}`}`);
