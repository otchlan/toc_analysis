
### Ta funkcja pobiera URLe
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


---

import pdfplumber
import json

def extract_table_of_contents(pdf_path):
    toc = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            # Extract text and annotations
            text = page.extract_text()
            annotations = page.annots if page.annots else []

            # Debugging: Print text and annotations
            print(f"--- Page {page_number + 1} Text ---\n{text}")
            print(f"--- Page {page_number + 1} Annotations ---\n{annotations}")

            # Process text
            if text:
                lines = text.split('\n')
                for line in lines:
                    if 'https://docs.llamaindex.ai/en/stable/' in line:
                        parts = line.split('https://docs.llamaindex.ai/en/stable/')
                        title = parts[0].strip()  # Extract the title from the first part
                        url = 'https://docs.llamaindex.ai/en/stable/' + parts[1].strip()
                        toc.append({'title': title, 'url': url})
                        print("URL: " + url)
            
            # Process annotations
            for annot in annotations:
                if 'uri' in annot:
                    url = annot['uri']
                    title = annot.get('title', 'No Title')
                    if title:
                        title = title.strip()
                    toc.append({'title': title, 'url': url})

    return toc

def save_to_json(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

pdf_path = 'toc.pdf'  # Replace with your PDF file path
toc_data = extract_table_of_contents(pdf_path)
save_to_json(toc_data, 'table_of_contents.json')

print("Table of contents saved to 'table_of_contents.json'")


---



import pdfplumber
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_table_of_contents(pdf_path):
    toc = []
    logging.info(f"Opening PDF file: {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                logging.info(f"Extracting text from page {page_number + 1}")
                lines = text.split('\n')
                for line in lines:
                    print(f"Line: {line}")  # Debugging: print each line
                    # Modify the condition below based on the actual structure of your PDF
                    if 'https://docs.llamaindex.ai/en/stable/' in line:
                        # Add logic to parse title and URL
                        toc.append({'title': 'Extracted Title', 'url': 'Extracted URL'})
            else:
                logging.warning(f"No text extracted from page {page_number + 1}")
    return toc

def save_to_json(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        logging.info(f"Saved table of contents to '{file_name}'")

pdf_path = 'toc.pdf'  # Replace with your PDF file path
toc_data = extract_table_of_contents(pdf_path)
save_to_json(toc_data, 'table_of_contents.json')



# pdf_processing.py
import pdfplumber
import json
import re
import pandas as pd

def is_item_starter(line):
    # Check if the line starts with a digit or roman numeral followed by a dot and space
    digit_based = re.match(r'^\d+\.\s', line)
    roman_numeral_based = re.match(r'^[ivxlcdm]+\.\s', line, re.IGNORECASE)
    return digit_based or roman_numeral_based

def split_line(line):
    # Split the line into a numeric/roman numeral prefix and the rest of the line
    match = re.match(r'^(\d+\.|\w+\.)\s*(.*)', line)
    if match:
        return match.groups()
    return None, None

def extract_items(pdf_path):
    items = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if is_item_starter(line):
                        prefix, title = split_line(line)
                        items[prefix] = {"title": title, "url": "No URL"}
            else:
                print(f"No text extracted from page {page.page_number}")

    return items

def save_to_json(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def display_json_as_table(file_name):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)

    df = pd.DataFrame([(key, value['title'], value['url']) for key, value in data.items()], columns=['Prefix', 'Title', 'URL'])
    print(df)

if __name__ == '__main__':
    pdf_path = 'toc.pdf'  # Replace with your PDF file path
    items_data = extract_items(pdf_path)
    save_to_json(items_data, 'table_of_contents.json')
    print("Items saved to 'table_of_contents.json'")

    file_name = 'table_of_contents.json'  # Replace with your JSON file name
    display_json_as_table(file_name)
