import fitz  # PyMuPDF
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGIndexer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.pdf_texts = self.extract_text_from_pdfs()
        self.vectorizer, self.vectors = self.index_texts()

    def extract_text_from_pdfs(self):
        pdf_texts = {}
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.folder_path, filename)
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                pdf_texts[filename] = text
        return pdf_texts

    def index_texts(self):
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2), stop_words='english')
    
        vectors = vectorizer.fit_transform(self.pdf_texts.values())
        return vectorizer, vectors

    def query_index_top_1(self, query):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors).flatten()

        # Debugging: Print similarities
        print(f"Query: {query}")
        print(f"Similarities: {similarities}")

        most_similar_idx = np.argmax(similarities)
        most_similar_pdf = list(self.pdf_texts.keys())[most_similar_idx]

        # Debugging: Print most similar PDF
        print(f"Most similar PDF: {most_similar_pdf}")

        return most_similar_pdf, self.pdf_texts[most_similar_pdf]
    
    def query_index(self, query, top_n=1):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.vectors).flatten()
        
        # Get the indices of the top N most similar PDFs
        top_n_indices = np.argsort(similarities)[-top_n:][::-1]
        top_n_pdfs = [(list(self.pdf_texts.keys())[i], similarities[i]) for i in top_n_indices]
        
        return top_n_pdfs    