// Function to open the cancel modal and pass any relevant data
function openCancelModal(serialNr) {
  const cancelModal = document.getElementById('cancelModal');
  cancelModal.style.display = 'block';
  cancelModal.setAttribute('data-serial-nr', serialNr);  // Store serial number (or any identifier) for later use
}

// Function to close the cancel modal
function closeCancelModal() {
  const cancelModal = document.getElementById('cancelModal');
  cancelModal.style.display = 'none';
  document.getElementById('cancelReason').value = '';  // Clear input field after closing the modal
}

// Function to handle form submission for canceling the request
function submitCancellation() {
  const cancelModal = document.getElementById('cancelModal');
  const serialNr = cancelModal.getAttribute('data-serial-nr');  // Get the stored serial number
  const cancelReason = document.getElementById('cancelReason').value;

  if (!cancelReason) {
    alert('Please provide a reason for cancellation.');
    return; // Don't submit if no reason is provided
  }

  // Proceed with cancellation logic (send to server or handle as needed)
  console.log(`Canceling request for serial number: ${serialNr}`);
  console.log(`Reason for cancellation: ${cancelReason}`);

  // Example: Sending a POST request to the server with the cancellation data
  fetch(`/it/hrs/cancel/${serialNr}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ reason: cancelReason }),
  })
    .then((response) => {
      if (response.ok) {
        closeCancelModal(); // Close the modal on success
        setTimeout(() => {
            window.location.reload();   // Reload the page after successful cancellation
        }, 500);
      } else {
        alert('Failed to cancel the request. Please try again.');
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while canceling the request.');
    });
}

// Adding event listeners for the modal buttons
document.getElementById('confirmCancelButton').addEventListener('click', submitCancellation);
document.querySelector('.exit-button').addEventListener('click', closeCancelModal);
