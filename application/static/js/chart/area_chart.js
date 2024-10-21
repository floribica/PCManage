document.addEventListener('DOMContentLoaded', function() {
    // Confirmed payments data
    const totalHrsDataElement = document.getElementById('total-hrss');
    const totalHrsData = JSON.parse(totalHrsDataElement.value || '[]');
  
    // Unconfirmed payments data
    const totalPcActionDataElement = document.getElementById('total-pc-actions');
    const totalPcActionData = JSON.parse(totalPcActionDataElement.value || '[]');
  
    // Check if data is valid
    if (!Array.isArray(totalHrsData) || totalHrsData.length === 0 ||
        !Array.isArray(totalPcActionData) || totalPcActionData.length === 0) {
      console.error('No data available for the chart.');
      return;
    }
  
    // Extract labels (e.g., months)
    const labels = totalHrsData.map(item => item.month); // Assume both datasets have the same months
  
    // Extract data for confirmed and unconfirmed payments
    const hrsData = totalHrsData.map(item => item.total_reuest);
    const pcActionData = totalPcActionData.map(item => item.total_pc_action);
  
    // Create the combined area chart
    const ctx = document.getElementById('combined-area-chart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'HR Request',
            data: hrsData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            tension: 0.3 // Smoothing of the line
          },
          {
            label: 'Prepared Set',
            data: pcActionData,
            backgroundColor: 'rgba(255, 99, 132, 0.2)', // Different color for unconfirmed
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 2,
            fill: true,
            pointRadius: 5,
            pointBackgroundColor: 'rgba(255, 99, 132, 1)',
            tension: 0.3 // Smoothing of the line
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });
  