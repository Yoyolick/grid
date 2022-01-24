table = document.getElementById("root"); //.getElementsByTagName('tbody')[0];
/*
for (let i = 0; i < 10000; i++) {
    //row 1
    if (i == 0) {
        table.insertAdjacentHTML('beforeend', '<tr id="column_1">');
        column1 = document.getElementById("column_1");
    }
    if (i > 0 && i <= 100) {
        column1.insertAdjacentHTML('beforeend', '<td class="pixel" id="pixel_' + i + '"></td>')
    }

    //row 1
    if (i == 101) {
        table.getElementsByTagName('tbody')[0].insertAdjacentHTML('beforeend', '<tr id="column_2">');
        column2 = document.getElementById("column_2");
    }
    if (i > 100 && i <= 200) {
        column2.insertAdjacentHTML('beforeend', '<td class="pixel" id="pixel_' + i + '"></td>')
    }

    //row 3
    if (i == 201) {
        table.getElementsByTagName('tbody')[0].insertAdjacentHTML('beforeend', '<tr id="column_2">');
        column2 = document.getElementById("column_2");
    }
}
*/

function basicxhr(route, data) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://127.0.0.1:80/" + route);
        xhr.setRequestHeader("Accept", "apllication/json");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            //this is where its rejecting on mobile TODO HTTPS
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send(JSON.stringify(data));
    });
}


function refreshBoard() {
    try {
        for (let i = 0; i < 100; i++) {
            document.getElementById('column_' + i).remove();
        }
    } catch {
        //
    }
    fetch('http://127.0.0.1:80/get')
        .then(response => response.json())
        .then(data => {
            table.insertAdjacentHTML('beforeend', '<tr>');

            for (let i = 0; i < 100; i++) {
                table.getElementsByTagName('tbody')[0].insertAdjacentHTML('beforeend', '<tr id="column_' + i + '">');
                selectedcolumn = document.getElementById('column_' + i + '');
                for (let x = 1; x <= 100; x++) {
                    console.log(data[i * 100 + x - 1])
                    selectedcolumn.insertAdjacentHTML("beforeend", '<td onclick="changePixel(' + (i * 100 + x) + ')" class="pixel" style="background-color: ' + data[i * 100 + x - 1][1] + ';" id="pixel_' + (i * 100 + x) + '"></td>')
                }
            }
        });
}

refreshBoard()

function changePixel(id) {
    document.getElementById('pixel_' + id).style.backgroundColor = document.getElementById('colorpicker').value;
    data = {
        "id": String(id),
        "color": String(document.getElementById('colorpicker').value)
    }
    //console.log('set ' + id);
    basicxhr('change', data);
}

//pixelcanvas.live