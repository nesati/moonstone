"""

"""

import markdown

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

if __name__ == '__main__':
    # generate html
    html = HTML
    with open("README.md", encoding='UTF-8') as f:
        md = f.read()
    md = md.replace('[online demo](https://nesati.github.io/)', '')
    html += markdown.markdown(md)
    html += "</body></html>"

    # save html
    with open("index.html", 'w', encoding='UTF-8') as f:
        f.write(html)
