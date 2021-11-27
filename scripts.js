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
                { left: '$', right: '$', display: false },
            ],
            // • rendering keys, e.g.:
            throwOnError: false
        });
        const exp_field = element.querySelector('.expressions')
        element.querySelectorAll('.katex').forEach((entry, i) => {
            var line = document.createElement('p');
            line.id = `entry${i + 1}`;
            line.className = "entry";
            exp_field.appendChild(line);
            new_entry = entry.cloneNode(true);
            new_entry.id = `exp${i + 1}`;
            exp_field.querySelector(`#entry${i + 1}`).append(`${i + 1}: `)
            exp_field.querySelector(`#entry${i + 1}`).appendChild(new_entry)
        })
        let i = 1
        //console.log(/\$.*?\$/.test(exps))
        while (/\$.*?\$/.test(exps)) {
            exps = exps.replace(/\$.*?\$/, `~${i}~`)
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

    });

})