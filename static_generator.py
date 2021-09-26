"""

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
    <meta charset='UTF-8'>
</head>
<body>
"""

INSTRUCTIONS = "Začněte přečtením fráze *začátek* a přeskočením prvního sloupce. Pokračujte čtením z leva do prava, " \
               "přicemž navazující úryvky vět z jednotlivých sloupců můžete mezi sebou libovolně kombinovat a některé" \
               " sloupce lze vynechat. Až bude esej dostatečně dlouhá, ukončete ji frází *konec*. \n\n "

if __name__ == '__main__':
    # generate table
    data = json.load(open("data/fragmenty.json", encoding='UTF-8'))
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
    example = [data['start']]

    for _ in range(10):
        for idx, options in enumerate(data['fragments']):
            if len(example) == 1 and idx == 0:  # skip first fragment in first sentence because it is handled by START
                continue
            if not (idx in data['optional'] and random.random() > 0.1):  # sometimes (90%) skip optional things
                example.append(random.choice(options))

    example = ''.join(example) + data['end']

    # add no js example
    md_left = md.split("<noscript>")[0] + "<noscript>\n"
    md_right = '\n</noscript>' + md.split("</noscript>")[1]
    md = md_left + example + md_right

    with open("README.md", 'w', encoding='UTF-8') as f:
        f.write(md)

    # generate html
    html = HTML
    md = md.replace('[online demo](https://nesati.github.io/)', '')
    html += markdown.markdown(md)
    html += "</body></html>"

    # save html
    with open("index.html", 'w', encoding='UTF-8') as f:
        f.write(html)
