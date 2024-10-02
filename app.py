import streamlit as st
import os
from io import BytesIO
from rag_indexer import RAGIndexer
from gemini import GeminiLLM

# Initialize RAG Indexer
rag_indexer = RAGIndexer('student_pdfs')

def process_text_input_top_1(text):
    print(text)
    most_similar_pdf, most_similar_text = rag_indexer.query_index_top_1(text)
    print(most_similar_pdf)
    response = GeminiLLM.generate_response(text, most_similar_text)
    return f"{response}\n\nSource: {most_similar_pdf} \n\nText: {most_similar_text}"

def process_text_input_top_n(text):
    top_n_pdfs = rag_indexer.query_index(text, top_n=2)
    responses = []
    for pdf, similarity in top_n_pdfs:
        most_similar_text = rag_indexer.pdf_texts[pdf]
        response = GeminiLLM.generate_response(text, most_similar_text)
        # responses.append(f"{response}\n\nSource: {pdf} \n\nText: {most_similar_text}")
        responses.append(f"{response}\n\n[Source]:( {pdf})")
    return responses

# Streamlit app
st.title("Voice and Text Based Governemnt Scheme Matcher")

# Text input
text_input = st.text_input("Enter your text here:")
if text_input:
    print(text_input)
    response = process_text_input_top_1(text_input)
    st.write(response)
    # for response in process_text_input_top_n(text_input):
    #     st.write(response)