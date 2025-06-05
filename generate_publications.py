import bibtexparser
import latexcodec
import re

header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-DLBK1VQJ2J"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-DLBK1VQJ2J');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications</title>
    <title>Tyler Hennen, PhD</title>
    <link rel="stylesheet" href="cardstyles.css">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico"> 
    <link rel="manifest" href="/site.webmanifest">
</head>
<body>

<h2>Tyler Hennen's Publications</h2>

<!-- <a href="">Boring version/bibtex version?</a> -->

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
        open_access = '<p><span class="open-access">(Open Access)</span></p>'
    else:
        open_access = ''

    title = bibtex_text_to_html(entry.get('title', ''))

    # papers that also have arxiv versions (Hard-coded)
    if doi == '10.1063/5.0080532':
        arxiv = '2112.00192'
    elif doi == '10.1063/5.0047571':
        arxiv = '2102.05770'
    else:
        arxiv = entry.get('eprint', '')

    # Full-text available somewhere online
    # Not sure if I should be linking them
    if doi == 'ISCAS45731.2020.9181105':
        bootleg_url = "https://confcats-event-sessions.s3.amazonaws.com/iscas20/papers/1836.pdf"
    else:
        bootleg_url = ''

    doi_url = f"https://doi.org/{doi}"
    arxiv_url = f"https://arxiv.org/abs/{arxiv}"

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

    if publisher == 'Arxiv':
        publisher = 'arXiv'

    year = entry.get('year', '')
    month = entry.get('month', '')

    img_fn = doi if doi else arxiv
    img_fn = img_fn.replace('/', '_')

    if doi:
        url = doi_url
    elif arxiv:
        url = arxiv_url

    if doi and arxiv:
        secondary_link = f'<p><em><a href="{arxiv_url}" target="_blank" rel="noopener noreferrer" class="secondary-link">arXiv version</a></em></p>'
    else:
        secondary_link = ''

    # dumb 
    title = title.replace('Ns', 'ns')

    return f"""
                    <div class="card">
                    <a href="{url}" target="_blank" rel="noopener noreferrer" class="card-link"></a>
                    
                    <img src="img/{img_fn}.png" alt="" style="border: none; text-decoration: none;">
                    <div class="card-content">
                        <h3>{title}</h3>
                        <p>{authorlist}</p>
                        <p><em>{publisher}</em></p>{open_access}{secondary_link}
                        <p class="publication-date">{month} {year}</p>
                    </div>
                    </div>
    """

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