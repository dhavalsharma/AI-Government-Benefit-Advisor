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
    You are a helpful, knowledgeable, and empathetic scholarship advisor assisting students in finding the most relevant government scholarships based on their academic, economic, and geographic conditions.
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

    @staticmethod
    def generate_response(query, context):
        """
        Generate a response from the Gemini API based on the provided query and context.
        """
        # Initialize the Gemini API client
        genai.configure(api_key=GeminiLLM.API)
        
        # Create a chat model with the system prompt
        model = genai.GenerativeModel(
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            system_instruction=GeminiLLM.system_prompt
        )
        
        # Start a chat session
        chat_session = model.start_chat()
        
        # Send a message to the chat session and get the response
        response = chat_session.send_message(f'scholarship_text:{context}\nquery:{query}')
        
        # Return the text of the response
        return response.text
        
# Example usage
if __name__ == "__main__":
    # Define a query and context for the example
    query = "I am 19 years old. Which scholarship is available?"
    context = "The student is looking for scholarships available for 19-year-olds."
    
    # Generate a response using the GeminiLLM class
    response = GeminiLLM.generate_response(query, context)
    
    # Print the response
    print(response)