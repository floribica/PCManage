// Function to open the delete modal and store the serial number
function openDeleteModal(serialNr) {
    // Store the serial number in a data attribute for later use
    document.querySelector('#deleteModal').dataset.serialNr = serialNr;

    // Display the delete modal
    document.getElementById('deleteModal').style.display = 'block';
}

// Function to close the delete modal
function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

// Function to delete the computer
function deleteComputer() {
    const serialNr = document.querySelector('#deleteModal').dataset.serialNr;

    // AJAX request to delete the computer
    fetch(`/it/computers/delete/${serialNr}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to /it/computers if deleted successfully
        } else {
            return response.json(); // Get the JSON response if not redirected
        }
    })
    .then(data => {
        if (data && data.success) {
            // Remove the deleted row from the table
            const row = document.querySelector(`tr:has(td:contains("${serialNr}"))`);
            if (row) {
                row.parentNode.removeChild(row);
            }

            // Close the modal
            closeDeleteModal();
        } else {
            // Display the error message
            document.getElementById('deleteError').textContent = data.error;
        }
    })
}

// Attach the deleteComputer function to the delete button in the modal
document.getElementById('confirmDeleteButton').addEventListener('click', deleteComputer);
