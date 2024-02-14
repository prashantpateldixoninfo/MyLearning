// console.log("This is Promises");

let prom1 = new Promise((resolve, reject) => {
    let a = Math.random();
    if (a < 0.5) {
        reject("Rejected: No random number was not supporting you 01");
    } else {
        setTimeout(() => {
            console.log("Resolved: Yes I am done 01");
            resolve("Resolved: Prashant 01");
        }, 3000);
    }
});

let prom2 = new Promise((resolve, reject) => {
    let a = Math.random();
    if (a < 0.5) {
        reject("Rejected: No random number was not supporting you 02");
    } else {
        setTimeout(() => {
            console.log("Resolved: Yes I am done 02");
            resolve("Resolved: Prashant 02");
        }, 1000);
    }
});

// all --> Waits for all promises to resolve and returns the array of their results.
//         If any one fails, it becomes the error & all other result are ignored.
// allSettled --> Waits for all the promises to settled and resturn their results as
//                an array of objects with status and value.
// race --> Waits for the first promise to settled and its result/error becomes the outcome
// any --> Waits for first promise to fulfill(& not rejected), and it's result becomee the
//         the outcome. Throws Aggregate Error if all the promises are rejected.

let p3 = Promise.any([prom1, prom2]);
p3.then((a) => {
    console.log(a);
}).catch((err) => {
    console.log(err);
});
