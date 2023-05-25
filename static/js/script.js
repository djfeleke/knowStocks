/* implementing search functionaly */

const search_input = document.getElementById('search_string');
const results = document.getElementById('search_results');

let search_term = '';
let companies;

//get data
const fetchCompanies = async () => {
    const url = 'http://127.0.0.1:5000/search'
    companies = await fetch(url)
        .then(result => result.json());
};

const showCompanies = async () => {
    results.innerHTML = '';

    await fetchCompanies();

    const ul = document.createElement('ul');
    ul.classList.add('companies');

    companies
        .filter(company =>
            company.company_name.toLowerCase().includes(search_term.toLowerCase())
            || company.ticker_symbol.toLowerCase().includes(search_term.toLowerCase())
        )
        .forEach(company => {
            const li = document.createElement('li');
            li.classList.add('company_item');

            const compnay_info = document.createElement('p');
            compnay_info.innerText = company.company_name + "" + company.ticker_symbol;
            compnay_info.classList.add('company_info');

            li.appendChild(company_info);

            ul.appendChild(li);
        });

    results.appendChild(ul);
};

showCompanies();

search_input.addEventListener('input', e => {
    search_term = e.target.value;
    showCompanies();
});

/*hiding empty list items*/

const list_item = document.getElementsByTagName("li");
if (list_item.node.textContent.trim() === "") {
    list_item.style.display = none;
}

/*hiding open accordion upon click */

$(document).ready(function () {
    $('.collapse').collapse
});
