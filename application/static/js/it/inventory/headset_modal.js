let currentHeadsetId = null;

function openDeleteModal(headsetId) {
    currentHeadsetId = headsetId;
    document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}

document.getElementById("confirmDeleteButton").onclick = function () {
    if (currentHeadsetId) {
        // Perform the DELETE request using fetch
        fetch(`/it/headsets/delete/${currentHeadsetId}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (response.redirected) {
                // Redirect if the response is a redirect
                window.location.href = response.url;
            }
        })
        .catch(error => console.error('Error deleting headset:', error));
    }
};
