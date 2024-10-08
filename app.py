import streamlit as st
import os
from io import BytesIO
from rag_indexer import RAGIndexer
from gemini import GeminiLLM

# Initialize RAG Indexer with the path to the folder containing student PDFs
rag_indexer = RAGIndexer('student_pdfs')

def process_text_input_top_1(text):
    """
    Process the text input to find the most similar PDF and generate a response.
    
    Args:
        text (str): The input text to query.
    
    Returns:
        str: The generated response along with the source PDF.
    """
    # Query the RAG indexer for the most similar PDF and its text
    most_similar_pdf, most_similar_text = rag_indexer.query_index_top_1(text)
    
    # Generate a response using the Gemini LLM
    geminiLLM = GeminiLLM(most_similar_text)
    # Add a Gemini Chat history object to Streamlit session state
    if "chat" not in st.session_state:
        st.session_state.chat = geminiLLM.get_chat_session()
        
    response = geminiLLM.generate_response(text)
    
    # Return the response along with the source PDF
    # return f"{response}\n\nSource: {most_similar_pdf}"
    return response

def process_text_input_top_n(text):
    """
    Process the text input to find the top N most similar PDFs and generate responses.
    
    Args:
        text (str): The input text to query.
    
    Returns:
        list: A list of generated responses along with their source PDFs.
    """
    # Query the RAG indexer for the top N most similar PDFs
    top_n_pdfs = rag_indexer.query_index(text, top_n=2)
    
    # Initialize a list to store the responses
    responses = []
    
    # Iterate over the top N PDFs and generate responses
    for pdf, similarity in top_n_pdfs:
        # Get the text of the most similar PDF
        most_similar_text = rag_indexer.pdf_texts[pdf]
        
        # Generate a response using the Gemini LLM
        response = GeminiLLM.generate_response(text, most_similar_text)
        
        # Append the response along with the source PDF to the list
        # responses.append(f"{response}\n\n[Source: {pdf}]")
    
    # Return the list of responses
    return responses

# Streamlit app
st.title("Voice and Text Based Government Scheme Matcher")

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
# source https://github.com/robkerr/robkerrai-demo-code/blob/main/how-to-create-a-google-gemini-chatbot/main.py
def role_to_streamlit(role):
  if role == "model":
    return "assistant"
  else:
    return role

# Display chat messages from history above current input box
if 'chat' in st.session_state:
    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

# # Text input
# text_input = st.text_input("Enter your text here:")
# if text_input:
#     print(text_input)
#     response = process_text_input_top_1(text_input)
#     st.write(response)
#     # uncomment below to get top n responses
#     # for response in process_text_input_top_n(text_input):
#     #     st.write(response)

# Accept user's next message, add to context, resubmit context to Gemini
if prompt := st.chat_input("What would you like to know on government schemes?"):
    # Display user's last message
    st.chat_message("user").markdown(prompt)
    
    # Send user entry to Gemini and read the response
    response = process_text_input_top_1(prompt)

    # Display last 
    with st.chat_message("assistant"):
        st.markdown(response.text)