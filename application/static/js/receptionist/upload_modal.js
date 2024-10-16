function openUploadModal(pcActionId) {
    document.getElementById('uploadPdfModal').style.display = 'block';
    document.querySelector('.upload-modal-overlay').style.display = 'block';
    document.getElementById('pcActionId').value = pcActionId;
}

function closeUploadModal() {
    document.getElementById('uploadPdfModal').style.display = 'none';
    document.querySelector('.upload-modal-overlay').style.display = 'none';
}