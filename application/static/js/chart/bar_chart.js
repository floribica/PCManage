document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the JSON data from the hidden input
    const totalPcActionDataDataElement = document.getElementById('total-pc-action');
    const totalPcActionDataData = JSON.parse(totalPcActionDataDataElement.value || '[]');
  
    // Extract labels (months) and data (totals)
    const labels = totalPcActionDataData.map(item => item.month);
    const data = totalPcActionDataData.map(item => item.total_pc_action);
  
    // Create the bar chart
    const ctx = document.getElementById('morris-bar-chart').getContext('2d');
    const myBarChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Total Sets',
          data: data,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });
  