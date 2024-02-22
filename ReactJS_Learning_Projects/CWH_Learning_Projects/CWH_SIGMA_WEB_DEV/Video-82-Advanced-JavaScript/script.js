var a1 = 6;
console.log(a1);

const sleep = async () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(45);
        }, 1000);
    });
};

const sum = async (a, b, c) => {
    return a + b + c;
};

(async function main() {
    let aa = await sleep();
    console.log(aa);
    let bb = await sleep();
    console.log(bb);

    let [x, y, rest] = [1, 5, 7, 8, 9, 10];
    console.log(x, y, rest);

    let obj = {
        a: 1,
        b: 2,
        c: 3,
    };

    let { a, b } = obj;
    console.log(a, b);

    let arr = [1, 4, 6];
    console.log(sum(arr[0], arr[1], arr[2]));
    console.log(sum(...arr));
})();
