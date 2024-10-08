"""
This file defines a GeminiLLM class that interacts with the Gemini API to provide scholarship advice.
The class loads environment variables, including the API key, and defines system prompts to guide the interaction.
The system prompts include instructions for gathering student information and providing tailored scholarship recommendations.
"""

import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

class GeminiLLM:
    # Load the API key from environment variables
    API = os.getenv('GEMINI_API_KEY')
    
    # Define the system prompt for general guidance
    system_prompt = """
    You are a helpful, knowledgeable, and empathetic scholarship advisor assisting students in 
    finding the most relevant government scholarships based on their academic, economic, and 
    geographic conditions.

    Government scheme context: {context}
    - Provide Tailored Scholarship Recommendations:
        - Name of scholarship
        - Deadline
        - Amount
        - Reservations
        - Number of scholarships
        - Application form requirements
        - Contact details
    """
    
    # Define the system prompt for gathering student information and providing recommendations
    system_prompt_1 = """
    - Gather Student Information:
      - Ask the student for their academic background (current level of education, GPA, field of study, certifications or achievements).
      - Inquire about their financial situation (household income, whether they are eligible for financial aid or needs-based scholarships).
      - Ask about their geographic location (country, region, or state they reside in) and if they are eligible for any local or regional scholarships.
      - Consider any additional personal factors (minority status, first-generation student, leadership experience, extracurricular activities).

    - Provide Tailored Scholarship Recommendations:
    """
    #create init method configures gemini with the API key and sets up model with system prompt
    def __init__(self, schemeContext):
        genai.configure(api_key=GeminiLLM.API)
        self.model = genai.GenerativeModel(
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            system_instruction = GeminiLLM.system_prompt.format(context=schemeContext),
            )
        
        # Start a chat session
        self.chat_session = self.model.start_chat(history=[])
    
    #generate_response method generates response from the Gemini API based on the provided query and context
    def generate_response(self, query):
        """
        Generate a response from the Gemini API based on the provided query and context.
        """
        # Send a message to the chat session and get the response
        response = self.chat_session.send_message(query)
        
        # Return the text of the response
        return response.text
        
# Example usage
if __name__ == "__main__":
    # Define a query and context for the example
    query = "I am 19 years old. Which scholarship is available?"
    context = "The student is looking for scholarships available for 19-year-olds."
    
    # Generate a response using the GeminiLLM class
    gemini_llm = GeminiLLM(context)
    response = gemini_llm.generate_response(query)
    # Print the response
    print(response)