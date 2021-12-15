document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-link').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.target.className = 'btn btn-link link-primary';
            e.target.parentElement.parentElement.className = '';
            const modal = document.querySelector('.modal-content');
            modal.innerHTML = '';
            fetch(`/message/${e.target.dataset.id}`)
                .then((response) => response.text())
                .then((html) => {
                    modal.innerHTML = html;
                });
        });
    });
});
