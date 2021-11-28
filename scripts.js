document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".editor").forEach(element => {
        const info_field = element.querySelector(".info p");
        const input_field = element.querySelector(".input");
        const render_field = element.querySelector(".render");
        var exps = info_field.innerText;
        input_field.dispatchEvent(new Event('input'))
        renderMathInElement(element.querySelector(".info"), {
            // customised options
            // • auto-render specific keys, e.g.:
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
            ],
            // • rendering keys, e.g.:
            throwOnError: false
        });
        const exp_field = element.querySelector('.expressions')
        element.querySelectorAll('.katex').forEach((entry, i) => {
            var line = document.createElement('li');
            line.id = `entry${i + 1}`;
            line.className = "entry";
            exp_field.appendChild(line);
            new_entry = (entry.parentElement.className === "katex-display" ? entry.parentElement : entry).cloneNode(true);
            new_entry.id = `exp${i + 1}`;
            exp_field.querySelector(`#entry${i + 1}`).appendChild(new_entry)
        })
        let i = 1
        //console.log(/\$.*?\$/.test(exps))
        while (/\$+.*?\$+/.test(exps)) {
            exps = exps.replace(/\$+.*?\$+/, `~${i}~`)
            console.log(i)
            i++;
        }
        input_field.innerText = exps

        input_field.addEventListener('input', (e) => {
            render_field.innerHTML = e.currentTarget.innerHTML
            element.querySelectorAll(".entry").forEach((e, i) => {
                const index_match = new RegExp(`~${i + 1}~`)
                while (index_match.test(render_field.innerHTML)) {
                    render_field.innerHTML = render_field.innerHTML.replace(`~${i + 1}~`, document.querySelector(`#exp${i + 1}`).outerHTML)
                }
            })
            // renderMathInElement(render_field, {
            //     // customised options
            //     // • auto-render specific keys, e.g.:
            //     delimiters: [
            //         { left: '~', right: '~', display: false },
            //     ],
            //     // • rendering keys, e.g.:
            //     throwOnError: false
            // });
        })
        input_field.dispatchEvent(new Event('input'))

        // Nivo Burns solution to move the caret to the end of the contenteditable:
        //https://stackoverflow.com/questions/1125292/how-to-move-cursor-to-end-of-contenteditable-entity/3866442#3866442
        range = document.createRange();//Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(input_field);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection();//get the selection object (allows you to change selection)
        selection.removeAllRanges();//remove any selections already made
        selection.addRange(range);//make the range you have just created the visible selection
    });

})