window.addEventListener("DOMContentLoaded", (event) => {
    // GET FORM INPUT ELEMENT
    const input = document.getElementById("input");
    // DISPLAY CITY NAMES ON KEYUP
    if (input) {
        input.addEventListener("keyup", display_cities);
    }
});

function display_cities() {
    const DEV_API_KEY = '65c24925b20ea7affe14f468-f503579fa35f';
    var url = new URL(`https://api.dev.me/v1-list-cities?x-api-key=${DEV_API_KEY}`);
    var data = {
        name: input.value,
    }
    Object.keys(data).forEach(key => url.searchParams.append(key, data[key]))
    fetch(url)
        .then(response => response.json())
        .then(json => {
            let names = Array()
            let arr = json['list']
            for (const element of arr) {
                names.push(element['name'] + ", " + element['countryName'])
            }
            const myList = document.getElementById("myList");
            const input = document.getElementById("input");
            myList.innerHTML = "";
            myList.style.visibility = "visible";
            const min = Math.min(names.length, 5)
            let i;
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