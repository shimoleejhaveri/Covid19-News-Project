
let endpoint1 = 'newsBySentiment'    //{% url "new-sentiment" %}

$.ajax({
  method:'GET',
  url:endpoint1,
  success: function(data){
    const chartsContainer = $('#chart1'); 
    const canvas = $('<canvas></canvas>');
    chartsContainer.append(canvas);

    const list_colors = ["#3cba9f", "#FF0000", "#3e95cd"]
    // "#8e5ea2", , "#e8c3b9", "#c45850"
    const list_sent = Object.keys(data);
    const list_sum = Object.values(data)

    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: list_sent,
        datasets: [{
          label: "Number of news",
          backgroundColor: list_colors,
          data: list_sum
        }]
      },
      options: {
        title: {
          display: true,
          text: ''
        }
      }
    });
  },
  error:function(error_data){
    console.log(error_data)
  }    

})

let endpoint2 = 'newsByDate' 
$.ajax({
  method:'GET',
  url:endpoint2,
  success: function(data){
    console.log(data)
    const chartsContainer = $('#chart2'); 
    const canvas = $('<canvas></canvas>');
    chartsContainer.append(canvas);

    list_days = Object.keys(data)
    list_number_pos = []
    list_number_neg = []
    list_number_neu = []

    for (let day of Object.values(data)) {
        list_number_pos.push(day.positive)
        list_number_neg.push(day.negative)
        list_number_neu.push(day.neutral)
    }

    console.log(list_number_neu)

    window.chartColors = {
      red: 'rgb(255, 99, 132)',
      orange: 'rgb(255, 159, 64)',
      yellow: 'rgb(255, 205, 86)',
      green: 'rgb(51, 204, 51)',
      blue: 'rgb(54, 162, 235)',
      purple: 'rgb(153, 102, 255)',
      grey: 'rgb(201, 203, 207)'
    };

    let lineChartData = {
        labels: list_days,
        datasets: [{
            label: 'Positive ',
            borderColor: window.chartColors.green,
            backgroundColor: window.chartColors.green,
            fill: false,
            data: list_number_pos,
            yAxisID: 'y-axis-1',
        }, {
            label: 'Neutral ',
            borderColor: window.chartColors.blue,
            backgroundColor: window.chartColors.blue,
            fill: false,
            data: list_number_neu,
            yAxisID: 'y-axis-1'
        }, {
            label: 'Negative ',
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: list_number_neg,
            yAxisID: 'y-axis-1'
        }]
    };

    window.onload = function() {
        // let ctx = canvas.getContext('3d');
        window.myLine = Chart.Line(canvas, {
            data: lineChartData,
            options: {
                responsive: true,
                hoverMode: 'index',
                stacked: false,
                // title: {
                //     display: true,
                //     text: 'Chart.js Line Chart - Multi Axis'
                // },
                scales: {
                    yAxes: [{
                        type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'left',
                        id: 'y-axis-1',

                        // grid line settings
                        gridLines: {
                            drawOnChartArea: true, // only want the grid lines for one axis to show up
                        },
                    }],
                }
            }
        });
    };

  },
  error:function(error_data){
    console.log(error_data)
  }    

})
