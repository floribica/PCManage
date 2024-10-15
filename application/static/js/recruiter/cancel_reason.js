 // Function to open the cancel modal and fetch reason from backend
 function openCancelModal(element) {
    const hrId = element.getAttribute("data-hr-id"); // Get the hr_id

    // Example of fetching the reason from the backend
    fetch(`/get-cancel-reason/${hrId}`)
      .then(response => response.json())
      .then(data => {
        // Display the fetched reason in the modal
        document.getElementById("cancelReason").textContent = data.cancel_reason;
        
        // Show the modal and the overlay
        document.getElementById("cancelModal").style.display = "block";
        document.getElementById("modalOverlay").style.display = "block";
      })
      .catch(error => {
        console.error("Error fetching cancel reason:", error);
      });
  }

  // Function to close the cancel modal
  function closeCancelModal() {
    document.getElementById("cancelModal").style.display = "none";
    document.getElementById("modalOverlay").style.display = "none"; // Hide overlay
  }