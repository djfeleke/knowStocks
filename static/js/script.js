
const searchInput = document.querySelector('#search_string')
searchInput.addEventListener("input", (event) => {
    let value = event.target.value
    if (value && value.trim().length > 0) {
        value = value.trim().toLowerCase()

        setList(people.filter(person => {
            return person.name.includes(value)
        }))
    } else {
        clearList();
    }
});

function setList(results) {

    for (const person of results) {
        const resultItem = document.createElement('li')
        resultItem.classList.add('result-item')
        const text = document.createTextNode(person.name)
        resultItem.appendChild(text)
        list.appendChild(resultItem)
    }
}

function clearList() {
    while (list.firstChild) {
        list.removeChild(list.firstChild)
    }
}

let capital = document.querySelectorAll(".market_capital");
for (let i = 0; i < capital.length; i++) {
    let num = Number(capital[i].innerHTML)
        .toLocaleString('en');
    capital[i].innerHTML = num;
    capital[i].classList.add("currSign");
}

// Market news
