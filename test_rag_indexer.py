import unittest
from rag_indexer import RAGIndexer

class TestRAGIndexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rag_indexer = RAGIndexer('student_pdfs')

    def test_query_index(self):
        prompts = [
            "I am 19 year old. Which scholarship is available?",
            "I am a female engineering student. Are there any scholarships for women in engineering?",
            "What are the eligibility criteria for the AICTE Pragati Scholarship?",
            "Can international students apply for the MHRD scholarships?",
            "What is the application process for the National Scholarship Portal?",
            "Are there any scholarships available for students from economically weaker sections?",
            "What documents are required to apply for the AICTE Saksham Scholarship?",
            "Is there any scholarship for students pursuing a PhD in India?",
            "How can I apply for the UGC NET JRF scholarship?",
            "Are there any scholarships for students with disabilities?",
            "What is the deadline for applying to the PMSSS scholarship?"
        ]

        for prompt in prompts[:2]:
            print(f"Prompt: {prompt}")
            most_similar_pdf, most_similar_text = self.rag_indexer.query_index(prompt)
            print(f"Prompt: {prompt}")
            print(f"Most similar PDF: {most_similar_pdf}\n")
            self.assertIsNotNone(most_similar_pdf)
            self.assertIsNotNone(most_similar_text)

if __name__ == '__main__':
    unittest.main()