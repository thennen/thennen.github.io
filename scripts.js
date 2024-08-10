function sortTable(columnIndex, sortDirection = "asc") {
    var table, rows, switching, i, x, y, shouldSwitch, direction, switchCount = 0;
    table = document.getElementById("citationTable");
    switching = true;
    direction = sortDirection; 

    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];

            if (direction === "asc") {
                if (columnIndex === 3) {  
                    if (parseInt(x.innerHTML) > parseInt(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                } else {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else if (direction === "desc") {
                if (columnIndex === 3) {  
                    if (parseInt(x.innerHTML) < parseInt(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                } else {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount === 0 && direction === "asc") {
                direction = "desc";
                switching = true;
            }
        }
    }
}

function applyAuthorStyling() {
    const rows = document.querySelectorAll('.citation-table tbody tr');

    rows.forEach(row => {
        const authors = row.querySelector('td').textContent.split(', ');
        const newHtml = authors.map(author => {
            return `<span class="author">${author}</span>`;
        }).join(', ');

        row.querySelector('td').innerHTML = newHtml;
    });
}

function boldAuthor(authorName) {
    const authorElements = document.querySelectorAll('.citation-table .author');
    authorElements.forEach(authorEl => {
        if (authorEl.textContent.trim() === authorName) {
            authorEl.classList.add('author-bold');
        }
    });
}

function handleMouseOver(event) {
    const authorName = event.target.textContent.trim();
    const authorElements = document.querySelectorAll('.citation-table .author');
    authorElements.forEach(authorEl => {
        if (authorEl.textContent.trim() === authorName) {
            authorEl.classList.add('underline');
        }
    });
}

function handleMouseOut() {
    const authorElements = document.querySelectorAll('.citation-table .author');
    authorElements.forEach(authorEl => {
        authorEl.classList.remove('underline');
    });
}

function addEventListeners() {
    const authorElements = document.querySelectorAll('.citation-table .author');
    authorElements.forEach(authorEl => {
        authorEl.addEventListener('mouseover', handleMouseOver);
        authorEl.addEventListener('mouseout', handleMouseOut);
    });
}

window.onload = function() {
    applyAuthorStyling();
    boldAuthor("Tyler Hennen");
    sortTable(3, "desc");
    addEventListeners();
};