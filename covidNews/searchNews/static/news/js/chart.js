
let endpoint1 = 'newsBySentiment'

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
    const list_sum = Object.values(data);

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

    const chartsContainer = $('#chart2'); 
    const canvas = $('<canvas></canvas>');
    chartsContainer.append(canvas);
    console.log(data)
    

    list_days = (Object.keys(data)).sort()
    list_nember_p = []
    list_nember_neg = []
    list_nember_neu = []

    list_nember_p = [10, 12, 23, 20] 

    for (let day of Object.values(data)) {
      list_nember_p.push(day.positive)
      list_nember_neg.push(day.negative)
      list_nember_neu.push(day.neutral)
    };

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
            data: list_nember_p,
            yAxisID: 'y-axis-1'
        }, {
            label: 'Negative ',
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: list_nember_neg,
            yAxisID: 'y-axis-1'
        }]
    };

    new Chart(canvas, {
      type: 'line',
      data: lineChartData,
      options: {
          responsive: true,
          hoverMode: 'index',
          stacked: false,
          scales: {
              yAxes: [{
                  type: 'linear', 
                  display: true,
                  position: 'left',
                  id: 'y-axis-1',
                  gridLines: {
                      drawOnChartArea: true,
                  },
              }],
          }
      }
    });
  },
  error:function(error_data){
    console.log(error_data)
  }    

})
