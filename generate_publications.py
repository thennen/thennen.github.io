import bibtexparser
import latexcodec
import re
import json

header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-DLBK1VQJ2J"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-DLBK1VQJ2J');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tyler Hennen's Publications</title>
    <link rel="stylesheet" href="cardstyles.css">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/site.webmanifest">
</head>
<body>

<h2>Tyler Hennen's Publications</h2>

<br>

"""[1:]


footer = """
</body>
</html>
"""

# Load the BibTeX file with UTF-8 encoding
with open('bibliography.bib', 'r', encoding='utf-8') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Load the JSON file with UTF-8 encoding
with open('publication_summaries.json', 'r', encoding='utf-8') as f:
    summaries = json.load(f)

entries = bib_database.entries

month_order = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
               "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

# Sort by year (descending) and month (descending)
entries = sorted(entries, key=lambda x: (
    -int(x.get('year', 0)),
    -month_order.get(x.get('month', '').strip().lower(), 0)
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

def bibtex_entry_to_html(entry, summaries_data):
    authorstring = entry.get('author', '')
    authorlist = ', '.join([' '.join(author.split(', ')[::-1]) for author in authorstring.split(' and ')])
    authorlist = bibtex_text_to_html(authorlist)
    authorlist = authorlist.replace("Tyler Hennen", "<strong>Tyler Hennen</strong>")
    authorlist = authorlist.replace(' ', '&nbsp;').replace('-', '&#8209;').replace(',&nbsp;', ', ')
    doi = entry.get('doi', '')

    annotation = entry.get('annotation')
    open_access = '<p><span class="open-access">(Open Access)</span></p>' if annotation and 'Open-access' in annotation else ''

    title = bibtex_text_to_html(entry.get('title', ''))
    title = title.replace('Ns', 'ns')

    if doi == '10.1063/5.0080532':
        arxiv = '2112.00192'
    elif doi == '10.1063/5.0047571':
        arxiv = '2102.05770'
    else:
        arxiv = entry.get('eprint', '')

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
    publisher = 'arXiv' if publisher == 'Arxiv' else publisher

    year = entry.get('year', '')
    month = entry.get('month', '')

    img_fn = doi if doi else arxiv
    img_fn = img_fn.replace('/', '_')

    doi_is_arxiv = 'arxiv' in doi.lower()

    url = doi_url if doi else arxiv_url

    if (doi and arxiv) and not doi_is_arxiv:
        secondary_link = f'<p><em><a href="{arxiv_url}" target="_blank" rel="noopener noreferrer" class="secondary-link">arXiv version</a></em></p>'
    else:
        secondary_link = ''

    # --- Generate Summary HTML Block ---
    summary_data = summaries_data.get(doi, {})
    simple_summary = summary_data.get('simple_summary', '')
    detailed_summary = summary_data.get('detailed_summary', '')
    summary_html = ""

    if simple_summary and detailed_summary:
        # Sanitize DOI for use in HTML attributes
        safe_doi = doi.replace('.', '_').replace('/', '_')
        radio_name = f"summary-level-{safe_doi}"

        summary_html = f"""
                        <div class="summary-container-tabs">
                            <input type="radio" name="{radio_name}" id="s-radio-1-{safe_doi}" class="summary-radio" checked>
                            <input type="radio" name="{radio_name}" id="s-radio-2-{safe_doi}" class="summary-radio">
                            <div class="summary-tabs">
                                <label for="s-radio-1-{safe_doi}">Short summary</label>
                                <label for="s-radio-2-{safe_doi}">Long summary</label>
                            </div>
                            <div class="summary-panels">
                                <div id="panel-1-{safe_doi}" class="summary-panel">
                                    {simple_summary}
                                </div>
                                <div id="panel-2-{safe_doi}" class="summary-panel">
                                    {detailed_summary}
                                </div>
                            </div>
                        </div>
                        """

    return f"""
                    <div class="card">
                        <a href="{url}" target="_blank" rel="noopener noreferrer" class="card-link"></a>
                        <img src="img/{img_fn}.png" alt="" style="border: none; text-decoration: none;">
                        <div class="card-content">
                            <h3>{title}</h3>
                            <p>{authorlist}</p>
                            <p><em>{publisher}</em></p>{open_access}{secondary_link}
                            <p class="publication-date">{month} {year}</p>
                            {summary_html}
                        </div>
                    </div>
    """

if __name__ == '__main__':
    with open('publications.html', 'w', encoding='utf-8') as f:
        f.writelines(header)
        for entry in entries:
            # Pass the summaries dictionary to the function
            f.writelines(bibtex_entry_to_html(entry, summaries))
        f.writelines(footer)