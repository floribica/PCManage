let currentmonitorId = null;

function openDeleteModal(monitorId) {
    currentmonitorId = monitorId;
    document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}

document.getElementById("confirmDeleteButton").onclick = function () {
    if (currentmonitorId) {
        // Perform the DELETE request using fetch
        fetch(`/it/monitors/delete/${currentmonitorId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.redirected) {
                // Redirect if the response is a redirect
                window.location.href = response.url;
            }
        })
        .catch(error => console.error('Error deleting monitor:', error));
    }
};
