document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-btn').forEach((btn) =>
        btn.addEventListener('click', (e) => {
            const form = e.target.parentElement.previousElementSibling;
            if (e.target.innerText === 'Edit') {
                e.target.innerText = 'Save';
                form.querySelectorAll('input, select').forEach((i) => {
                    i.style.display = 'block';
                });
                form.querySelectorAll('span').forEach((i) => {
                    i.style.display = 'none';
                });
            } else {
                e.target.disable = true;
                let csrftoken = getCookie('csrftoken');
                fetch('/update', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrftoken },
                    body: JSON.stringify({
                        // correctly treating the different personal info edits
                        info:
                            form.querySelectorAll('input').length > 0
                                ? // parsing out the fields to an JSON fields
                                  [...form.querySelectorAll('input')].reduce(
                                      (a, v) => ({ ...a, [v.name]: v.value }),
                                      {}
                                  )
                                : form.querySelectorAll('select').length > 0 &&
                                  //parsing out the multiple selects to the correct fields as arrays
                                  [...form.querySelectorAll('select')].reduce(
                                      (a, v) => ({
                                          ...a,
                                          [v.name]: [...v.options]
                                              .filter((l) => l.selected)
                                              .map((l) => l.value),
                                      }),
                                      {}
                                  ),
                    }),
                })
                    .then((response) => response.json())
                    .then((result) => {
                        if ('error' in result) {
                            alert('Something went wrong');
                        } else {
                            e.target.innerText = 'Edit';
                            e.target.disable = false;
                            form.querySelectorAll('span').forEach((i) => {
                                i.innerText =
                                    form.querySelectorAll('input').length > 0
                                        ? i.parentElement.querySelector('input')
                                              .value
                                        : [
                                              ...i.parentElement.querySelector(
                                                  'select'
                                              ).options,
                                          ]
                                              .filter((l) => l.selected)
                                              .map((l) => l.innerText)
                                              .join(', ');
                                i.style.display = 'block';
                            });
                            form.querySelectorAll('input').forEach((i) => {
                                i.style.display = 'none';
                            });
                            form.querySelectorAll('select').forEach((i) => {
                                i.style.display = 'none';
                            });
                        }
                    });
            }
        })
    );
    //disabling selected options to avoid selections in both active and secondary.
    const fselectors = document.querySelectorAll('.lang-update');
    const opts = fselectors[1].querySelectorAll('option');
    fselectors[0].addEventListener('change', () => {
        opts.forEach((opt) => {
            opt.disabled = [...fselectors[0].options]
                .filter((l) => l.selected)
                .map((l) => l.value)
                .includes(opt.value);
        });
        opts.forEach((opt) => {
            if (opt.disabled && opt.selected) {
                fselectors[1].value = [...opts].filter(
                    (opt) => !opt.disabled
                )[0].value;
            }
        });
    });
});
