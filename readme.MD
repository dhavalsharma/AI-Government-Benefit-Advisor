# SSMGS-GenAI App

SSMGS-GenAI: Sri Sri Meri Government Scheme is an AI-powered platform that helps individuals discover and access government schemes tailored to their needs.

## Setup

1. Clone the repository.
2. Build the Docker image: `docker build -t my-streamlit-app .`
3. Run the Docker container: `docker run -p 8501:8501 my-streamlit-app`

## Usage

Open your browser and navigate to `http://localhost:8501`.

Some of the prompts you can try are 
- I am a high school senior with 81% marks. My family has a low income, and we live in Uttar Pradesh. I'm interested in studying computer science. Are there any government scholarships I qualify for?
- I am a first-year college student with a 3.5 GPA. My family is from a rural area in Maharashtra, and we have a low income. I'm studying mechanical engineering. What government scholarships are available for me?
- I am a high school junior with 75% marks. My family is from a minority community in Karnataka, and we have a low income. I want to pursue a degree in civil engineering. Are there any government scholarships I can apply for?
- I am a second-year college student with a 3.8 GPA. My family lives in a tribal area in Odisha, and we have a low income. I'm studying electrical engineering. What government scholarships can I apply for?

For more prompt samples, see [test_rag_indexer.py](test_rag_indexer.py).
