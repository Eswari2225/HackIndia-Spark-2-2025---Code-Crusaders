fetch('/compliance_data')
  .then(response => response.json())
  .then(data => {
    // Update the chart and alerts with the received data
  });