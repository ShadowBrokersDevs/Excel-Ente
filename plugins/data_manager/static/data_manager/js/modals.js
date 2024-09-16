function openRenameModal(dbName) {
    document.querySelector('#rename-form input[name="db_name"]').value = dbName;
    document.getElementById('current_db_name').innerText = dbName;
    document.getElementById('rename-modal').classList.remove('hidden');
}

function closeRenameModal() {
    document.getElementById('rename-modal').classList.add('hidden');
}

function openDeleteModal(dbId) {
    document.getElementById('confirm-delete').onclick = function() {
        window.location.href = `/data-manager/database/delete/${dbId}/`;
    };
    document.getElementById('delete-modal').classList.remove('hidden');
}

function closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('hidden');
}

function openInfoModal(dbId) {
    fetch(`/data-manager/database/info/${dbId}/`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('info-content').innerHTML = data;
            document.getElementById('info-modal').classList.remove('hidden');
        });
}

function closeInfoModal() {
    document.getElementById('info-modal').classList.add('hidden');
}
