//simple script to send an 'offer' to a user
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.offer-btn').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            let csrftoken = getCookie('csrftoken');
            fetch(`/offer`, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: JSON.stringify({
                    user_id: e.target.dataset.id,
                }),
            });
        });
    });
});
