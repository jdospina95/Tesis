var ctx = document.getElementById("myChart").getContext('2d');
var myBarChart;
var chartType = 'bar';
var data = {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [{
            label: '% de Aciertos',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    }
var options = {
    scales: {
       yAxes: [{
           ticks: {
               min: 0,
               max: 100,
               callback: function(value) {
                   return value + "%"
               }
           }
       }]
    }
}

// var myDoughnutChart = new Chart(ctx, {
//     type: 'doughnut',
//     data: {
//         datasets: [{
//         data: [10, 20, 30]
//     }],

//     // These labels appear in the legend and in the tooltips when hovering different arcs
//     labels: [
//         'Red',
//         'Yellow',
//         'Blue'
//     ]},
//     options: {
//         animation: {
//             duration: 0, // general animation time
//         },
//         hover: {
//             animationDuration: 0, // duration of animations when hovering an item
//         },
//         responsiveAnimationDuration: 0, // animation duration after a resize
//     }
// });

init();

function init() {
  // Chart declaration:
  myBarChart = new Chart(ctx, {
    type: chartType,
    data: data,
    options: options
  });
}

function toggleChart(chartType) {
  //destroy chart:
  myBarChart.destroy();
  //change chart type: 
  this.chartType = chartType;
  //restart chart:
  init();
}