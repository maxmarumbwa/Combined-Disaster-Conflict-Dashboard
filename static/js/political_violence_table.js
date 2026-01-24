let currentPage = 1;
let pageSize = 20;

const tableBody = document.querySelector("#data-table tbody");
const pageInfo = document.getElementById("page-info");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

function loadTable(page = 1) {
    const url = `/api/table/?page=${page}&page_size=${pageSize}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            renderTable(data.results);
            updatePagination(data, page);
        })
        .catch(err => console.error(err));
}

function renderTable(rows) {
    tableBody.innerHTML = "";

    rows.forEach(row => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${row.province}</td>
            <td>${row.year}</td>
            <td>${row.month}</td>
            <td>${row.events}</td>
            <td>${row.fatalities}</td>
        `;

        tableBody.appendChild(tr);
    });
}

function updatePagination(data, page) {
    currentPage = page;

    pageInfo.textContent = `Page ${currentPage}`;

    prevBtn.disabled = data.previous === null;
    nextBtn.disabled = data.next === null;
}

prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        loadTable(currentPage - 1);
    }
});

nextBtn.addEventListener("click", () => {
    loadTable(currentPage + 1);
});

// Initial load
loadTable();
