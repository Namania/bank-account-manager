const element = document.getElementById("json");
const json = JSON.parse(element.innerText);

const data = {
    labels: json["labels"],
    datasets: [{
        data: json["data"],
        backgroundColor: json["backgroundColor"],
    }]
};

const options = {
    legend: {
        display: false,
    },
    plugins: {
        annotation: {
            annotations: {
                dLabel: {
                    type: 'doughnutLabel',
                    content: ({chart}) => [
                        'Total',
                        'adzda',
                        'last 7 months'
                    ],
                    font: [{size: 60}, {size: 50}, {size: 30}],
                    color: ['black', 'red', 'grey']
                }
            }
        }
    }
};

const config = {
    type: 'doughnut',
    data: data,
    options
};

window.onload = function() {
    var ctx = document.getElementById('pie-chart').getContext('2d');
    window.myPie = new Chart(ctx, config);
};