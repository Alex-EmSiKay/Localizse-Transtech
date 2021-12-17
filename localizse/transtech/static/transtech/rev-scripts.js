document.addEventListener('DOMContentLoaded', () => {
    editor = document.querySelector('.editor');
    const pk = document.querySelector('#pk').innerHTML;
    const info_field = editor.querySelector('.info p');
    const input_field = editor.querySelector('.input');
    const render_field = editor.querySelector('.render');
    var exps = input_field.innerText;
    trans_exps = [...exps.matchAll(/\$+.*?\$+/g)];
    //runs KaTeX to render the maths info/original content.
    renderMathInElement(editor.querySelector('.info'), {
        // customised options
        // • auto-render specific keys, e.g.:
        delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
        ],
        // • rendering keys, e.g.:
        throwOnError: false,
    });
    // pulling the new katex elements in the info and formatting them
    // into the expressions sections
    const exp_field = editor.querySelector('.expressions');
    editor.querySelectorAll('.katex').forEach((entry, i) => {
        var line = document.createElement('li');
        line.id = `entry${i + 1}`;
        line.className = 'entry';
        exp_field.appendChild(line);
        new_entry = (
            entry.parentElement.className === 'katex-display'
                ? entry.parentElement
                : entry
        ).cloneNode(true);
        new_entry.id = `exp${i + 1}`;
        exp_field.querySelector(`#entry${i + 1}`).appendChild(new_entry);
    });
    //updating the input field with the expression 'tags'.
    let i = 1;
    while (/\$+.*?\$+/.test(exps)) {
        exps = exps.replace(/\$+.*?\$+/, `~${i}~`);
        i++;
    }
    input_field.innerText = exps.trim();
    // takes the current input and renders the math based on the position of the tags
    input_field.addEventListener('input', (e) => {
        render_field.innerHTML = e.currentTarget.innerHTML;
        var incomplete = false;
        // input control to make sure all the tags are represented correctly.
        editor.querySelectorAll('.entry').forEach((e, i) => {
            const index_match = new RegExp(`~${i + 1}~`, 'g');
            incomplete = incomplete
                ? true
                : (input_field.innerText.match(index_match) || []).length !== 1;
            while (index_match.test(render_field.innerHTML)) {
                render_field.innerHTML = render_field.innerHTML.replace(
                    `~${i + 1}~`,
                    document.querySelector(`#exp${i + 1}`).outerHTML
                );
            }
            document.querySelector('.save-btn').disabled =
                incomplete || /~/.test(render_field.innerText) ? true : false;
        });
    });
    input_field.dispatchEvent(new Event('input'));

    // Nivo Burns solution to move the caret to the end of the contenteditable:
    //https://stackoverflow.com/questions/1125292/how-to-move-cursor-to-end-of-contenteditable-entity/3866442#3866442
    range = document.createRange(); //Create a range (a range is a like the selection but invisible)
    range.selectNodeContents(input_field); //Select the entire contents of the element with the range
    range.collapse(false); //collapse the range to the end point. false means collapse to end rather than the start
    selection = window.getSelection(); //get the selection object (allows you to change selection)
    selection.removeAllRanges(); //remove any selections already made
    selection.addRange(range); //make the range you have just created the visible selection

    const save_btn = document.querySelector('.save-btn');
    const skip_btn = document.querySelector('.skip-btn');
    save_btn.addEventListener('click', () => {
        if (save_btn.innerText === 'Edit') {
            input_field.parentElement.parentElement.style.display = 'block';
            save_btn.innerText = 'Save';
            if (approve_btn !== null) {
                approve_btn.style.display = 'none';
            }
            input_field.focus();
        } else {
            save_btn.disabled = true;
            var new_exps = input_field.innerText;
            trans_exps.forEach((exp, i) => {
                const index = new RegExp(`~${i + 1}~`, 'g');
                new_exps = new_exps.replace(index, exp);
            });
            let csrftoken = getCookie('csrftoken');
            fetch('/save', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: JSON.stringify({
                    content: new_exps,
                    content_id: pk,
                    type: location.pathname.replace('/work/', ''),
                }),
            })
                .then((response) => response.json())
                .then((result) => {
                    if ('error' in result) {
                        alert('Something went wrong');
                    } else {
                        input_field.parentElement.parentElement.style.display =
                            'none';
                        save_btn.innerText = 'Edit';
                        save_btn.disabled = false;
                        skip_btn.innerHTML = 'Next item';
                    }
                });
        }
    });
    const approve_btn = document.querySelector('.approve-btn');
    if (approve_btn !== null) {
        approve_btn.addEventListener('click', () => {
            approve_btn.style.display = 'none';
            save_btn.innerText = 'Save';
            save_btn.dispatchEvent(new Event('click'));
        });
    }
});
