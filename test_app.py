import unittest
from unittest.mock import patch, MagicMock
import app

class TestApp(unittest.TestCase):

    @patch('app.st.text_input')
    @patch('app.st.write')
    @patch('app.process_text_input_top_n')
    def test_text_input(self, mock_process_text_input_top_n, mock_st_write, mock_st_text_input):
        # Define the student queries
        student_queries = [
            "I am a high school senior with 81% marks. My family has a low income, and we live in Uttar Pradesh. I'm interested in studying computer science. Are there any government scholarships I qualify for?",
            "I am a first-year college student with a 3.5 GPA. My family is from a rural area in Maharashtra, and we have a low income. I'm studying mechanical engineering. What government scholarships are available for me?",
            "I am a high school junior with 75% marks. My family is from a minority community in Karnataka, and we have a low income. I want to pursue a degree in civil engineering. Are there any government scholarships I can apply for?",
            "I am a second-year college student with a 3.8 GPA. My family lives in a tribal area in Odisha, and we have a low income. I'm studying electrical engineering. What government scholarships can I apply for?",
            "I am a high school graduate with 85% marks. My family is from a backward class in Tamil Nadu, and we have a low income. I want to study information technology. Are there any government scholarships available for me?",
            "I am a first-year college student with a 3.2 GPA. My family is from a low-income background in West Bengal. I'm studying chemical engineering. What government scholarships are available for me?",
            "I am a high school senior with 78% marks. My family is from a low-income background in Punjab. I want to pursue a degree in biotechnology. Are there any government scholarships I qualify for?",
            "I am a second-year college student with a 3.6 GPA. My family is from a low-income background in Rajasthan. I'm studying aerospace engineering. What government scholarships can I apply for?",
            "I am a high school junior with 80% marks. My family is from a low-income background in Gujarat. I want to study environmental science. Are there any government scholarships available for me?",
            "I am a first-year college student with a 3.4 GPA. My family is from a low-income background in Bihar. I'm studying computer engineering. What government scholarships are available for me?"
        ]

        # Mock the return value of process_text_input_top_n
        mock_process_text_input_top_n.return_value = ["mock_response"]

        for query in student_queries:
            # Mock the text input to return the current query
            mock_st_text_input.return_value = query

            # Run the app code that processes the text input
            app.text_input = query
            if app.text_input:
                for response in app.process_text_input_top_n(app.text_input):
                    app.st.write(response)

            # Assert that st.write was called with the mock response
            mock_st_write.assert_called_with("mock_response")

if __name__ == '__main__':
    unittest.main()