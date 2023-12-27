# Opis projektu
Celem jest zbudowanie funkcji, która/e będą z podanego pliku (toc.pdf) poobierać listę nazw rozdziałów oraz linki.
Następnie dane te łączyć w jeden plik .json, plik ten będzie potem dalej rozbudowywany o treść już z linków.

**Docelowo ma to wyglądać tak**
Najważniejsze jest, aby title i url były poprawnie mapowane i zapisywane razem
~~~
    "28.": {
        "title": "Multi-Document Agents (V1)",
        "url": "https://docs.llamaindex.ai/en/stable/module_guides/querying/output_parser.html"
    },
~~~
**!** 28 jest ważne, jest to mapowanie kolejności ze spisu treści mogą się też trafiać "a,b,c", "i, ii, ..., vi"(coś tu jest nie tak z mapowaniem, ale to już na ludzie później ogarnę) 



# Stan obecny
~~~
pdf_prodessing.py
~~~
Główna funkcja. 

Jej zadaniem jest zwrócić bibliotekę danych, mam problem z połączeniem jej do kupy

~~~
def extract_items
~~~
Funkcja ta układa słownik, ale nie zbiera URL
~~~
    "28.": {
        "title": "Multi-Document Agents (V1)",
        "url": "No  URL"
    },
    "29.": {
        "title": "FLARE Query Engine",
        "url": "No  URL"
    },
~~~

~~~
def merge_urls_into_items
~~~
Ta funkcja powinna dodawać do powyższego słownika "url"

~~~

ID: 429, URL: https://docs.llamaindex.ai/en/stable/module_guides/querying/output_parser.html
ID: 430, URL: https://docs.llamaindex.ai/en/stable/examples/output_parsing/GuardrailsDemo.html
~~~

# PROJEKTOWY.py
Znajduje się tu czysta funkcja pobierająca urle, w razie co
~~~
import pdfplumber

def extract_urls_from_pdf_annotations(pdf_path):
    urls = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            annotations = page.annots if page.annots else []
            for annot in annotations:
                if annot and 'uri' in annot:
                    url = annot['uri']
                    if isinstance(url, bytes):
                        url = url.decode('utf-8')  # Decode if it's in bytes
                    urls.append(url)

    return urls

# Usage example
pdf_path = 'your_pdf_file.pdf'  # Replace with your actual PDF file path
extracted_urls = extract_urls_from_pdf_annotations(pdf_path)

# Print the extracted URLs
for url in extracted_urls:
    print(url)

~~~