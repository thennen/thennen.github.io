import bibtexparser
import latexcodec
import re

header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications</title>
    <title>Tyler Hennen, PhD</title>
    <link rel="stylesheet" href="cardstyles.css">
</head>
<body>

<h2>Publications</h2>

<!-- <a href="">Boring version</a> -->

<br>

"""[1:]


footer = """
</body>
</html>
"""




with open('bibliography.bib', 'r') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

entries = bib_database.entries
# TODO: try to also sort by month
#entries = sorted(entries, key=lambda x:x.get('year'), reverse=True)

month_order = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
               "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

# Sort by year (descending) and month (descending)
entries = sorted(entries, key=lambda x: (
    -int(x.get('year', 0)),  # Negative for descending order
    -month_order.get(x.get('month', '').strip().lower(), 0)  # Negative for descending order
))

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
    authorlist = authorlist.replace("Tyler Hennen", "<strong>Tyler Hennen</strong>")
    authorlist = authorlist.replace(' ', '&nbsp;').replace('-', '&#8209;').replace(',&nbsp;', ', ')
    doi = entry.get('doi', '')
    
    annotation = entry.get('annotation')
    if annotation and 'Open-access' in annotation: # Just some thing I did in Zotero to mark it manually
        open_access = '<span class="open-access"> (Open Access)</span>'
    else:
        open_access = ''

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

    year = entry.get('year', '')
    month = entry.get('month', '')

    links = ''
    if doi:
        links += f'<a href="https://doi.org/{doi}", target="_blank" rel="noopener noreferrer" class="journal-link">link</a>'
    if arxiv:
        links += f'<a href="https://arxiv.org/abs/{arxiv}", target="_blank" rel="noopener noreferrer" class="arxiv">arXiv</a>'

    img_fn = doi if doi else arxiv
    img_fn = img_fn.replace('/', '_')


    if doi:
        url = f"https://doi.org/{doi}"
    elif arxiv:
        url = f"https://arxiv.org/abs/<arxiv>"


    # dumb 
    title = title.replace('Ns', 'ns')


    return f"""
                    <a href="{url}", target="_blank" rel="noopener noreferrer" class="card">
                    <img src="img/{img_fn}.png" alt="" style="border: none; text-decoration: none;">
                    <div class="card-content">
                        <h3>{title}</h3>
                        <p>{authorlist}</p>
                        <p><em>{publisher}</em>{open_access}</p>
                        <p class="publication-date">{month} {year}</p>
                    </div>
                    </a>
    """


if __name__ == '__main__':
    with open('publications.html', 'w', encoding='utf-8') as f:
        f.writelines(header)
        for entry in entries:
            f.writelines(bibtex_entry_to_html(entry))
        f.writelines(footer)