window.addEventListener("DOMContentLoaded", (event) => {
    // GET FORM INPUT ELEMENT
    const input = document.getElementById("input");
    // DISPLAY CITY NAMES ON KEYUP
    if (input) {
        input.addEventListener("keyup", display_cities);
    }
});

function display_cities() {
    var url = new URL(`https://api.teleport.org/api/cities/`);
    var data = {
        search: input.value,
        format: 'json'
    }
    Object.keys(data).forEach(key => url.searchParams.append(key, data[key]))
    fetch(url)
        .then(response => response.json())
        .then(json => {
            let names = Array()
            let arr = json['_embedded']['city:search-results']
            for (const element of arr) {
                names.push(element['matching_full_name'])
            }
            const myList = document.getElementById("myList");
            const input = document.getElementById("input");
            myList.innerHTML = "";
            myList.style.visibility = "visible";
            const min = Math.min(names.length, 5)
            for (i = 0; i < min; ++i) {
                let li = document.createElement('li');
                li.innerText = names[i];
                li.onclick = function () {
                    input.value = li.innerHTML;
                    myList.innerHTML = "";
                };
                myList.appendChild(li);
            }
            console.log(json);
            console.log(names);
        })
        .catch(err => console.error(err));
}