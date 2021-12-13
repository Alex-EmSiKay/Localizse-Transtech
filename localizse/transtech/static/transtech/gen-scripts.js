document.addEventListener('DOMContentLoaded', () => {
    const selectors = document.querySelectorAll('.lang-select select');
    if (selectors.length > 1) {
        const opts = selectors[1].querySelectorAll('option');
        selectors[0].addEventListener('change', () => {
            opts.forEach((opt) => {
                opt.disabled = selectors[0].value === opt.value;
            });
            opts.forEach((opt) => {
                if (opt.disabled && opt.selected) {
                    selectors[1].value = [...opts].filter(
                        (opt) => !opt.disabled
                    )[0].value;
                }
            });
        });
        selectors[0].dispatchEvent(new Event('change'));
        selectors.forEach((selector) => {
            selector.addEventListener('change', () => {
                document.querySelector('#lang-btn').style.display = 'block';
            });
        });
    }
    const lang_btn = document.querySelector('#lang-btn');
    lang_btn.addEventListener('click', () => {
        lang_btn.disabled = true;
        let csrftoken = getCookie('csrftoken');
        fetch('/setlang', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: JSON.stringify({
                primary: selectors[0].value,
                secondary: selectors[1].value,
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if ('error' in result) {
                    alert('Something went wrong');
                    lang_btn.disabled = false;
                } else {
                    location.reload();
                }
            });
    });
});
