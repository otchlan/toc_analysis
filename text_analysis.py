# text_analysis.py
from neo4j import GraphDatabase
from databases.neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

class TextAnalysis:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, 
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def extract_keywords(self, text):
        nltk.download('punkt')
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        keywords = [word for word in words if word.isalpha() and word not in stop_words]
        return keywords

    def add_text_to_graph(self, url, text):
        with self.driver.session() as session:
            keywords = self.extract_keywords(text)
            session.write_transaction(self._add_data, url, keywords)

    @staticmethod
    def _add_data(tx, url, keywords):
        query = (
            "MERGE (p:Page {url: $url}) "
            "FOREACH (word IN $keywords | "
            "   MERGE (k:Keyword {name: word}) "
            "   MERGE (p)-[:CONTAINS]->(k))"
        )
        tx.run(query, url=url, keywords=keywords)


def extract_labels_and_descriptions(content):
    # Simple text processing to extract labels and descriptions
    # This is a basic example and might need to be adapted for complex data
    labels = re.findall(r'\b[A-Z][a-z]*\b', content)  # Find words starting with a capital letter
    description = content[:150]  # Get the first 150 characters as a description
    return labels, description

