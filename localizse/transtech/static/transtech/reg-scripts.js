document.addEventListener('DOMContentLoaded', () => {
    const selectors = document.querySelectorAll('.form-lang-select select');
    const opts = selectors[1].querySelectorAll('option');
    selectors[0].addEventListener('change', () => {
        opts.forEach((opt) => {
            opt.disabled = [...selectors[0].options]
                .filter((l) => l.selected)
                .map((l) => l.value)
                .includes(opt.value);
        });
        opts.forEach((opt) => {
            if (opt.disabled && opt.selected) {
                selectors[1].value = [...opts].filter(
                    (opt) => !opt.disabled
                )[0].value;
            }
        });
    });
    document.querySelector('form').addEventListener('submit', (e) => {
        e.preventDefault();
        //input control to make sure the correct amount of languages are picked
        if (
            [...selectors[0].options].filter((l) => l.selected).length < 1 ||
            [...selectors[0].options].filter((l) => l.selected).length +
                [...selectors[1].options].filter((l) => l.selected).length <
                2
        ) {
            alert(
                'You must choose at least one primary language and at least two languages overall'
            );
        } else {
            e.target.submit();
        }
    });
});
