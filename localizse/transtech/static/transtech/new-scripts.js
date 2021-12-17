document.addEventListener('DOMContentLoaded', () => {
    editor_container = document.querySelector('.editor');
    const input_field = editor_container.querySelector('.input');
    const render_field = editor_container.querySelector('.render');
    const save_btn = editor_container.querySelector('.save');
    input_field.addEventListener('input', () => {
        //updating the render and runs KaTeX to render the maths.
        if (input_field.innerText !== '') {
            render_field.innerText = input_field.innerText;
            renderMathInElement(render_field, {
                // customised options
                // • auto-render specific keys, e.g.:
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '$', right: '$', display: false },
                ],
                // • rendering keys, e.g.:
                throwOnError: false,
            });
        } else {
            render_field.innerText = 'Rendered content will appear here';
        }
        // input control: disables the save button if there are any common errors
        // in the input, including trailing '$' and invalid LaTeX.
        if (
            (input_field.innerText.match(/(?<!\\)\$/g) || []).length % 2 ||
            render_field.querySelectorAll(
                'span[style="color: rgb(204, 0, 0);"]'
            ).length > 0 ||
            render_field.innerText.match(/\$\$/)
        ) {
            save_btn.disabled = true;
        } else {
            save_btn.disabled = false;
        }
    });
    input_field.dispatchEvent(new Event('input'));
    input_field.addEventListener('blur', () => {
        input_field.innerText = input_field.innerText;
    });
    //updating the interface on a successful save
    save_btn.addEventListener('click', () => {
        if (save_btn.innerText === 'Edit') {
            const msg = document.querySelector('.message');
            msg.style.display = 'none';
            save_btn.parentElement.removeChild(
                save_btn.parentElement.querySelector('a')
            );
            input_field.parentElement.parentElement.style.display = 'block';
            save_btn.innerText = 'Save';
            input_field.focus();
        } else {
            save_btn.disabled = true;
            let csrftoken = getCookie('csrftoken');
            fetch('/save', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: JSON.stringify({
                    language: document.querySelectorAll(
                        '.lang-select select'
                    )[0].value,
                    content: input_field.innerText,
                    // the id of the content is recorded after save so the user can make any
                    // quick edits directly after saving.
                    content_id: typeof pk === 'undefined' ? null : pk,
                }),
            })
                .then((response) => response.json())
                .then((result) => {
                    const msg = document.querySelector('.message');
                    msg.style.display = 'block';
                    if ('message' in result) {
                        msg.innerText = 'Saved successfully!';
                        input_field.parentElement.parentElement.style.display =
                            'none';
                        save_btn.innerText = 'Edit';
                        save_btn.disabled = false;
                        create_link = document.createElement('a');
                        create_link.className = 'btn btn-primary m-1';
                        create_link.href = 'create';
                        create_link.role = 'button';
                        create_link.innerHTML = 'Create new';
                        save_btn.parentElement.appendChild(create_link);
                        pk = result.content_id;
                    } else {
                        msg.innerText = 'Something went wrong';
                        save_btn.disabled = false;
                    }
                });
        }
    });
});
