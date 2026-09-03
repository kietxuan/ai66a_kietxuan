async function greet() {
    return "Hello, World!";
}

console.log(greet()); 

//c1
function getData1() {
    let text = "";
    greet().then(response => {
        text = response;
    });
    return text; 
}
console.log(getData1());

//c2
async function getData() {
    const text = await greet();
    console.log(text);
}

getData();
/*
function fetchUsers() {
    fetch('https://jsonplaceholder.typicode.com/users')
        .then((response) => {return response.json();})
        .then(users => {
            let tableBody = document.querySelector('#user-table tbody');
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.email.toLowerCase()}</td>
                    <td>${user.phone}</td>
                    <td>${user.website}</td>
                    <td>${user.address.city + "-" + user.address.street}</td>`;
                    //
                tableBody.appendChild(row);
            });
        });
}
*/

async function fetchUsers() {
    const response = await fetch('https://jsonplaceholder.typicode.com/users');
    const users = await response.json();
    let tableBody = document.querySelector('#user-table tbody');
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email.toLowerCase()}</td>
            <td>${user.phone}</td>
            <td>${user.website}</td>
            <td>${user.address.city + "-" + user.address.street}</td>`;
        tableBody.appendChild(row);
    });
}
