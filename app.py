import streamlit as st
import os
from io import BytesIO
from rag_indexer import RAGIndexer
from gemini import GeminiLLM


class GovernmentSchemesChatbot:
    def __init__(self):
        # Initialize RAG Indexer with the path to the folder containing student PDFs
        self.rag_indexer = RAGIndexer('student_pdfs')
        self.sample_prompt = ""
        self.initialize_ui()

    def initialize_ui(self):
        st.title("Sri Sri Meri Government Schemes")

        with st.sidebar:
            self.display_form()
        self.handle_user_input()

    def display_form(self):
        with st.form(key='user_form'):
            gender = st.selectbox("Gender", ["male", "female", "other"], index=1)
            age = st.number_input("Age", min_value=0, max_value=100, value=18)
            academic_background = st.text_input("Academic Background", "high school with 85% marks")
            family_income = st.number_input("Family Income in LPA", min_value=0, max_value=100, value=5)
            current_degree = st.text_input("Current Degree", "Bachelor of Engineering")
            institution = st.text_input("Institution (AICTE approved)", "VNIT Nagpur")
            response_language = st.selectbox(
                "Response Language", 
                ["English", "Hindi", "Tamil", "Telugu", "Bengali", "Marathi", 
                 "Kannada", "Malayalam", "Gujarati", "Urdu"]
            )
            submit_button = st.form_submit_button(label='Generate Sample Prompt')
            
            if submit_button:
                self.sample_prompt = (
                    f"I am a {gender} student with an age of {age} years and a "
                    f"family income of {family_income} LPA. "
                    f"My academic background is {academic_background}. "
                    f"I am studying {current_degree} "
                    f"at {institution}. What government scholarships are available for me?"
                    f"please reply in {response_language}"
                )
                st.write(f"{self.sample_prompt}")

    def handle_user_input(self):
        self.display_history()
        # Accept user's next message, add to context, resubmit context to Gemini
        input_question = "What would you like to know on government schemes?"
        if (len(self.sample_prompt) > 0):
            #todo add the sample prompt to the chat, it does not take as yet 
            prompt = self.sample_prompt

        if prompt := st.chat_input(input_question):
            
            # Display user's last message
            self.display_user_message(prompt)
            
            # Send user entry to Gemini and read the response
            response = self.process_text_input_top_1(prompt)

            # Display last response
            self.display_assistant_message(response.text)

    def display_user_message(self, message):
        st.chat_message("user").markdown(message)

    def display_assistant_message(self, message):
        with st.chat_message("assistant"):
            st.markdown(message)

    def display_history(self):
        # Display chat messages from history above current input box
        if 'chat' in st.session_state:
            for message in st.session_state.chat.history:
                with st.chat_message(self.role_to_streamlit(message.role)):
                    st.markdown(message.parts[0].text)

    # Gemini uses 'model' for assistant; Streamlit uses 'assistant'
    # source https://github.com/robkerr/robkerrai-demo-code/blob/main/how-to-create-a-google-gemini-chatbot/main.py
    def role_to_streamlit(self, role):
        if role == "model":
            return "assistant"
        else:
            return role

    def process_text_input_top_1(self, text):
        """
        Process the text input to find the most similar PDF and generate a response.
        
        Args:
            text (str): The input text to query.
        
        Returns:
            str: The generated response along with the source PDF.
        """
        # Query the RAG indexer for the most similar PDF and its text
        most_similar_pdf, most_similar_text = self.rag_indexer.query_index_top_1(text)
        
        # Generate a response using the Gemini LLM
        geminiLLM = GeminiLLM(most_similar_text)
        # Add a Gemini Chat history object to Streamlit session state
        if "chat" not in st.session_state:
            st.session_state.chat = geminiLLM.get_chat_session()
            
        response = geminiLLM.generate_response(text)
        
        # Return the response along with the source PDF
        # return f"{response}\n\nSource: {most_similar_pdf}"
        return response

    def process_text_input_top_n(self, text):
        """
        Process the text input to find the top N most similar PDFs and generate responses.
        
        Args:
            text (str): The input text to query.
        
        Returns:
            list: A list of generated responses along with their source PDFs.
        """
        # Query the RAG indexer for the top N most similar PDFs
        top_n_pdfs = self.rag_indexer.query_index(text, top_n=2)
        
        # Initialize a list to store the responses
        responses = []
        
        # Iterate over the top N PDFs and generate responses
        for pdf, similarity in top_n_pdfs:
            # Get the text of the most similar PDF
            most_similar_text = self.rag_indexer.pdf_texts[pdf]
            
            # Generate a response using the Gemini LLM
            response = GeminiLLM.generate_response(text, most_similar_text)
            
            # Append the response along with the source PDF to the list
            # responses.append(f"{response}\n\n[Source: {pdf}]")
        
        # Return the list of responses
        return responses

# # Text input
# text_input = st.text_input("Enter your text here:")
# if text_input:
#     print(text_input)
#     response = process_text_input_top_1(text_input)
#     st.write(response)
#     # uncomment below to get top n responses
#     # for response in process_text_input_top_n(text_input):
#     #     st.write(response)


if __name__ == "__main__":
    GovernmentSchemesChatbot()