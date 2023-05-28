/* implementing search functionaly */
function searchCompany() {
    let filter = document.getElementById("filter").value.toLowerCase();
    let companyRecord = document.getElementById("all_companies");
    let tr = companyRecord.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            let textvalue = td.textContent || td.innerHTML;
            if (textvalue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            else {
                tr[i].style.display = "none";
            }

        }
    }
}
function searchReginalCompany() {
    let filter = document.getElementById("filter").value.toLowerCase();
    let companyRecord = document.getElementById("reginal_companies");
    let tr = companyRecord.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            let textvalue = td.textContent || td.innerHTML;
            if (textvalue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            }
            else {
                tr[i].style.display = "none";
            }

        }
    }
}
/*
const search_input = document.getElementById('search_string');
const results = document.querySelector('#search_results');

let search_term = "";
let companies;

//get data

function fetchCompanies() {
    fetch('/search')
        .then((response) => response.json())
        .then((data) => {
            companies = data.map(x => x.company_name);
            companies.sort();
            showCompanies(companies, results)
        })
};

function showCompanies(data, element) {
    if (data) {
        element.innerHTML = "";
        let innerElement = "";

        data.forEach((item) => {
            innerElement += `
            <li>${item}</li>`;
        });
        element.innerHTML = innerElement;
    }

    function filterData(data, search_term) {

        return data.filter(company =>
            company.company_name.toLowerCase().includes(search_term.toLowerCase())
            || company.ticker_symbol.toLowerCase().includes(search_term.toLowerCase())
        );
    }
}

fetchCompanies();

search_input.addEventListener('input', function () {
    const filteredData = filterData(companies, search_input.value);

    showCompanies(filteredData, results);
})
*/