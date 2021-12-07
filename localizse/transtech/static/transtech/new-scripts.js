document.addEventListener('DOMContentLoaded', () => {
    editor_container = document.querySelector(".editor")
    const input_field = editor_container.querySelector(".input");
    const render_field = editor_container.querySelector(".render");
    const save_btn = editor_container.querySelector(".save");
    input_field.addEventListener('input', () => {
        if (input_field.innerText !== "") {
            render_field.innerText = input_field.innerText;
            renderMathInElement(render_field, {
                // customised options
                // • auto-render specific keys, e.g.:
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '$', right: '$', display: false },
                ],
                // • rendering keys, e.g.:
                throwOnError: true
            });
        }
        else {
            render_field.innerText = "Rendered content will appear here"
        }
    })
    input_field.dispatchEvent(new Event('input'))
    input_field.addEventListener('blur', () => {
        input_field.innerText = input_field.innerText
    })
    save_btn.addEventListener('click', () => {
        let csrftoken = getCookie('csrftoken');
        fetch('/save', {
            method: 'POST',
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                language: 'EN',
                content: input_field.innerText
            })
        })
    })
})