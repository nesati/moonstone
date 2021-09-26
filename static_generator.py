"""
Why spend 6 minutes doing something when you can spend 6 hours failing to automate it?

Automatically updates readme and static webpage with updated fragments.json.
"""
import json

import markdown
import random
from itertools import zip_longest

HTML = """
<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <title>Generátor univerzálních esejí</title>
    <script src='data/generator.js'></script>
    <link rel='stylesheet' href='data/main.css'>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset='UTF-8'>
</head>
<body>
<a href="https://github.com/nesati/moonstone" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>
<noscript>Automatický generátor funguje jen s funkčním JavaScriptem.</noscript>
"""

INSTRUCTIONS = "Začněte přečtením fráze *začátek* a přeskočením prvního sloupce. Pokračujte čtením z leva do prava, " \
               "přicemž navazující úryvky vět z jednotlivých sloupců můžete mezi sebou libovolně kombinovat a některé" \
               " sloupce lze vynechat. Až bude esej dostatečně dlouhá, ukončete ji frází *konec*. \n\n "

if __name__ == '__main__':
    # generate table
    data = json.load(open("data/fragments.json", encoding='UTF-8'))
    table = "<table>\n"
    table += '<tr><td>' + '</td><td>'.join(["<i><b>lze vynechat</b></i>" if idx in data['optional'] else "" for idx in
                                            range(len(data['fragments']))]) + '</td></tr>\n'
    for row in zip_longest(*data['fragments'], fillvalue=''):
        table += '<tr><td>' + '</td><td>'.join(row) + '</td></tr>\n'
    table += "</table>"

    # generate instructions
    instructions = INSTRUCTIONS + f"Začátek: \"{data['start']}\"\n\nKonec: \"{data['end']}\"\n"

    # generate readme
    with open("README.md", encoding='UTF-8') as f:
        md = f.read()
    md_left = md.split("## Jak to funguje?")[0] + "## Jak to funguje?\n"
    md_right = '\n\n## Inspirace' + md.split("## Inspirace")[1]
    md = md_left + instructions + table + md_right

    # generate example
    example = data['start']

    for i in range(10):
        for idx, options in enumerate(data['fragments']):
            if i == 0 and idx == 0:  # skip first fragment in first sentence because it is handled by START
                continue
            if not (idx in data['optional'] and random.random() > 0.1):  # sometimes (90%) skip optional things
                example += random.choice(options)

    example += data['end']

    # add no js example
    md_left = md.split('<div id="script">')[0] + '<div id="script">\n'
    md_right = md.split('</div>')[2]
    md = md_left + '<div id="text"></div>\n</div>\n\n>' + example + md_right

    with open("README.md", 'w', encoding='UTF-8') as f:
        f.write(md)

    # generate html
    html = HTML
    md = md.replace('[online demo](https://nesati.github.io/moonstone)', '')
    html += markdown.markdown(md)
    html += "</body></html>"

    # save html
    with open("index.html", 'w', encoding='UTF-8') as f:
        f.write(html)
