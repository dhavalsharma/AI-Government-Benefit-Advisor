import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

class GeminiLLM:
    API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Define the system prompt
    system_prompt = """
    You are a helpful, knowledgeable, and empathetic scholarship advisor assisting students in finding the most relevant government scholarships based on their academic, economic, and geographic conditions.
"""
    system_prompt_1 = """
    - Gather Student Information:
      - Ask the student for their academic background (current level of education, GPA, field of study, certifications or achievements).
      - Inquire about their financial situation (household income, whether they are eligible for financial aid or needs-based scholarships).
      - Ask about their geographic location (country, region, or state they reside in) and if they are eligible for any local or regional scholarships.
      - Consider any additional personal factors (minority status, first-generation student, leadership experience, extracurricular activities).

    - Provide Tailored Scholarship Recommendations:
      - Analyze the student's responses and match them with the most relevant government scholarships.
      - Sort the scholarships by priority based on the student’s financial need, academic merit, and geographic location.
      - Provide key information about each scholarship (e.g., application deadlines, documents required, eligibility requirements).

    - Offer Additional Support:
      - Recommend other resources, such as tips on writing scholarship essays, or strategies to enhance their application.
      - Suggest the student keep track of deadlines and provide options to save scholarships for future reference.

    - Maintain a Supportive Tone:
      - Be encouraging and motivational, understanding that this process can be overwhelming.
      - Reassure the student that you are here to help them succeed and make the process as smooth as possible.

      The scholarship details will be in additional context starting with scholarship_text: and user's query will start with query:        
        """

    @staticmethod
    def generate_response(query, context):
        genai.configure(api_key=GeminiLLM.API_KEY)
        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            # safety_settings = Adjust safety settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            system_instruction=GeminiLLM.system_prompt
        )
        chat_session = model.start_chat()
        response = chat_session.send_message(f'scholarship_text:{context}\nquery:{query}')
        return response.text
        
# Example usage
if __name__ == "__main__":
    query = "I am 19 years old. Which scholarship is available?"
    context = "The student is looking for scholarships available for 19-year-olds."
    response = GeminiLLM.generate_response(query, context)
    print(response)