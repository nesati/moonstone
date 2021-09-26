const HTML = `
<label for="n_sent">Počet vět</label>
<input type="number" id="n_sent" value="10">
<button onclick="generate()">Vygenerovat</button>
<br><br>
<div id="text"></div>
`
window.addEventListener('load', e => {
    document.getElementsByTagName('blockquote')[0].innerHTML = HTML
})

let data = null
fetch('data/fragments.json').then(r => {
    r.json().then(fragments => {
        data = fragments
    });
});

function generate() {
    let text = document.getElementById('text')
    if (data === null) {
        text.innerHTML = "<i>Potřebná data nejsou stažená. Prosím zkuste to za chvíli.</i>"
    } else {
        const n_sent = parseInt(document.getElementById('n_sent').value)
        let esej = data['start']
        for (let i = 0;i<n_sent;i++) {
            data['fragments'].forEach((v, k) => {
                if(!(i === 0 && k === 0) && !(data['optional'].indexOf(k) >= 0 && Math.random() > 0.1)) {
                    esej += v[Math.floor(Math.random()*v.length)]
                }
            })
        }
        esej += data['end']
        text.innerText = esej
    }
}