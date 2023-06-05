// implementing user search 
const headers = {
    'Content-Type': 'application/json'
}

function userSearchCompany(company_id) {
    // alert(company_id)
    input = document.getElementById('filter').value;
    body = { 'company_id': company_id, 'input': input }

    fetch('/user_search', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: headers
    }).then(response => response.text())
        .then(data => {
            console.log(data)
        })
}




//fixing the navigation at the top
document.addEventListener("DOMContentLoaded", function () {
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            document.getElementById('navbar_top').classList.add('fixed-top');
            // add padding top to show content behind navbar
            navbar_height = document.querySelector('.navbar').offsetHeight;
            document.body.style.paddingTop = navbar_height + 'px';
        } else {
            document.getElementById('navbar_top').classList.remove('fixed-top');
            // remove padding top from body
            document.body.style.paddingTop = '0';
        }
    });
});

function applyFiltersAndSearch() {
    const selectedRegion = document.getElementById('filter_region').value;
    const selectedCategory = document.getElementById('filter_category').value;
    const selectedSector = document.getElementById('filter_sector').value;
    // let searchKeyword = document.getElementById('filter').value.toLowerCase();

    const rows = document.querySelectorAll('#all_companies tbody tr');

    for (let i = 0; i < rows.length; i++) {
        let category = rows[i].querySelector('td[data-category]').getAttribute('data-category');
        let region = rows[i].querySelector('td[data-region]').getAttribute('data-region');
        let sector = rows[i].querySelector('td[data-sector_name]').getAttribute('data-sector_name');
        // let company = rows[i].querySelector('td[data-company]').getAttribute('data-company').toLowerCase();


        let regionMatch = selectedRegion === '' || region === selectedRegion;
        let categoryMatch = selectedCategory === '' || category === selectedCategory;
        let sectorMatch = selectedSector === '' || sector === selectedSector;
        // var searchMatch = company.includes(searchKeyword);

        if (regionMatch && categoryMatch && sectorMatch) {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = 'none';
        }
    }
}

document.getElementById('filter_sector').addEventListener('change', applyFiltersAndSearch);
document.getElementById('filter_category').addEventListener('change', applyFiltersAndSearch);
document.getElementById('filter_region').addEventListener('change', applyFiltersAndSearch);
// document.getElementById('filter').addEventListener('input', applyFiltersAndSearch);

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

document.getElementById('filter_category').addEventListener('change', function () {
    const selectedOption = this.value;
    const rows = document.querySelectorAll('#all_companies tbody tr');

    for (let i = 0; i < rows.length; i++) {

        let category = rows[i].querySelector('td[data-category]').getAttribute('data-category');

        if (selectedOption === '' || category === selectedOption) {
            rows[i].style.display = '';
        }
        else {
            rows[i].style.display = 'none';
        }
    }
});

document.getElementById('filter_region').addEventListener('change', function () {
    const selectedOption = this.value;
    const rows = document.querySelectorAll('#all_companies tbody tr');

    for (let i = 0; i < rows.length; i++) {
        let region = rows[i].querySelector('td[data-region]').getAttribute('data-region');

        if (selectedOption === '' || region === selectedOption) {
            rows[i].style.display = '';
        }
        else {
            rows[i].style.display = 'none';
        }
    }
});
document.getElementById('filter_sector').addEventListener('change', function () {
    const selectedOption = this.value;
    const rows = document.querySelectorAll('#all_companies tbody tr');

    for (let i = 0; i < rows.length; i++) {

        let sector = rows[i].querySelector('td[data-sector_name]').getAttribute('data-sector_name');

        if (selectedOption === '' || sector === selectedOption) {
            rows[i].style.display = '';
        }
        else {
            rows[i].style.display = 'none';
        }
    }
});
*/