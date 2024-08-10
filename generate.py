import bibtexparser
import latexcodec
import re

header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tyler Hennen</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="table-container">
        <table class="citation-table" id="citationTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Authors</th>
                    <th onclick="sortTable(1)">Title</th>
                    <th onclick="sortTable(2)">Publisher</th>
                    <th onclick="sortTable(3)">Year</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
"""[1:]

footer = """
            </tbody>
        </table>
    </div>
    <script src="scripts.js"></script>
</body>
</html>
"""

with open('bibliography.bib', 'r') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

entries = bib_database.entries
# TODO: try to also sort by month
entries = sorted(entries, key=lambda x:x.get('year'), reverse=True)

def bibtex_text_to_html(bibtex_title: str) -> str:
    # Handle textsubscript commands
    html_title = re.sub(r'{\\textsubscript{([^{}]+)}}', r'<sub>\1</sub>', bibtex_title)
    html_title = re.sub(r'{\\textsuperscript{([^{}]+)}}', r'<sup>\1</sup>', html_title)
    html_title = html_title.replace('\\%', '%')
    html_title = html_title.encode('latex').decode('latex+utf-8')
    # Remove double curly brackets
    html_title = re.sub(r'{{([^{}]+)}}', r'\1', html_title)
    # Remove single curly brackets
    html_title = re.sub(r'{([^{}]+)}', r'\1', html_title)
    # Remove latex math $$
    html_title = re.sub(r'\$([^\$]+)\$', r'<i>\1</i>', html_title)
    return html_title

def bibtex_entry_to_html(entry):
    # Create an HTML row for the entry
    authorstring = entry.get('author', '')
    authorlist = ', '.join([' '.join(author.split(', ')[::-1]) for author in authorstring.split(' and ')])
    authorlist = bibtex_text_to_html(authorlist)
    doi = entry.get('doi', '')

    title = bibtex_text_to_html(entry.get('title', ''))


    if doi == '10.1063/5.0080532':
        arxiv = '2112.00192'
    elif doi == '10.1063/5.0047571':
        arxiv = '2102.05770'
    else:
        arxiv = entry.get('eprint', '')

    entry_type = entry.get('ENTRYTYPE')
    if entry_type == 'article':
        publisher = entry.get('journal', '')
    elif entry_type == 'inproceedings':
        publisher = entry.get('booktitle', '')
    elif entry_type == 'phdthesis':
        publisher = 'RWTH Aachen University'
    else:
        publisher = entry.get('publisher', '')

    publisher = bibtex_text_to_html(publisher)

    links = ''
    if doi:
        links += f'<a href="https://doi.org/{doi}", target="_blank" rel="noopener noreferrer">[doi]</a>'
    if arxiv:
        links += f'<a href="https://arxiv.org/abs/{arxiv}", target="_blank" rel="noopener noreferrer">[arXiv]</a>'

    return f"""
                <tr>
                    <td>{authorlist}</td>
                    <td>{title}</td>
                    <td>{publisher}</td>
                    <td>{entry.get('year', '')}</td>
                    <td>{links}</td>
                </tr>
    """


if __name__ == '__main__':
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(header)
        for entry in entries:
            f.writelines(bibtex_entry_to_html(entry))
        f.writelines(footer)