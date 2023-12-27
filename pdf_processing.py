import pdfplumber
import json
import re
from fuzzywuzzy import process

def is_item_starter(line):
    digit_based = re.match(r'^\d+\.\s', line)
    roman_numeral_based = re.match(r'^[ivxlcdm]+\.\s', line, re.IGNORECASE)
    return digit_based or roman_numeral_based

def split_line(line):
    match = re.match(r'^(\d+\.|\w+\.)\s*(.*)', line)
    return match.groups() if match else (None, None)

def extract_urls_from_pdf_annotations(pdf_path):
    url_mapping = {}
    url_id = 1  # Start with ID 1

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            annotations = page.annots if page.annots else []
            for annot in annotations:
                if annot and 'uri' in annot and annot.get('title'):
                    title = annot.get('title', '').strip()
                    url = annot['uri']
                    if isinstance(url, bytes):
                        url = url.decode('utf-8')  # Decode if it's in bytes
                    url_mapping[url_id] = url
                    url_id += 1  # Increment ID for the next URL

    return url_mapping


def merge_urls_into_items(items, url_mapping):
    for key, item in items.items():
        title = item.get('title')
        if title in url_mapping:
            item['url'] = url_mapping[title]

    return items



def extract_items(pdf_path):
    items = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            annotations = page.annots if page.annots else []

            if text:
                lines = text.split('\n')
                for line in lines:
                    if is_item_starter(line):
                        prefix, title = split_line(line)
                        url = "No  URL"
                        items[prefix] = {"title": title, "url": url}
            else:
                print(f"No text extracted from page {page.page_number + 1}")

    return items

def save_to_json(data, file_name):
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def display_json_as_table(file_name):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if isinstance(value, dict):
                # Assuming each value is a dictionary with 'title' and 'url'
                print(f"{key}: Title: {value.get('title', 'N/A')}, URL: {value.get('url', 'N/A')}")
            elif isinstance(value, list):
                # If the value is a list (like for 'Extracted URLs'), print each item in the list
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                # Handle other data types (if any)
                print(f"{key}: {value}")

def integrate_urls_into_items(items, urls):
    # Assuming that each URL contains a segment that matches a part of the title in items
    for key, item in items.items():
        for url in urls:
            if item['title'] in url:  # A simple check to match title with URL
                items[key]['url'] = url
                break  # Break the loop once a match is found
    return items

def main():
    pdf_path = 'toc.pdf'  # Replace with your PDF file path

    # Extract items
    items_data = extract_items(pdf_path)

    # Extract URL mapping from annotations
    url_mapping = extract_urls_from_pdf_annotations(pdf_path)

    # Merge URLs into items
    merged_items = merge_urls_into_items(items_data, url_mapping)

    # Save to JSON
    save_to_json(merged_items, 'table_of_contents.json')
    print("Items saved to 'table_of_contents.json'")



if __name__ == '__main__':
    main()