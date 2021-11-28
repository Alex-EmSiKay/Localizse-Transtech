document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".editor").forEach(element => {
        const input_field = element.querySelector(".input");
        const render_field = element.querySelector(".render");
        input_field.addEventListener('input', () => {
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
        })
        input_field.addEventListener('blur', () => {
            input_field.innerText = input_field.innerText
        })
    })
})