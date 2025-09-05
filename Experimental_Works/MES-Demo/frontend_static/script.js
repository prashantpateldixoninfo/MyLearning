// script.js
document.addEventListener("DOMContentLoaded", function () {
    fetch("http://localhost:8000/dashboard")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("resultsTable");
            data.forEach(row => {
                const r = table.insertRow();
                r.insertCell(0).innerText = row.serial_no;
                r.insertCell(1).innerText = row.test_type;
                r.insertCell(2).innerText = row.result;
                r.insertCell(3).innerText = new Date(row.timestamp).toLocaleString();
            });
        })
        .catch(err => console.error("Failed to load data:", err));
});
