# local imports
from Retriever import retriever

# external imports
import logging
import os
import requests
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
class LogIt:
    def __init__(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("Errors")
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        log_file_path = os.path.join(log_dir, "data_ingestion.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)

        self.logger = logger


logger = LogIt().logger

# Gemini API details
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Prompt template
prompt = PromptTemplate(
template="""You are a helpful assistant for students at the ECE department of NIT Hamirpur.
You are given the official curriculum documents, syllabus, and academic information for all years and semesters (1st to 4th year).

### Instructions:
- Your answer **must always fit within 1000 tokens**.
- When Needed give direct and short output.
- If the full syllabus or content is too long, **summarize or compress wording** while keeping all units/chapters/topics intact.
- Do **not leave answers half-cut**. Ensure the response is complete and self-contained.
- Focus only on the **relevant academic year/subject** mentioned in the question.
- If asked for syllabus or details, always show **all chapters/units**, but you may use **shortened phrases** to stay within the limit.
- If information is missing or ambiguous, respond with:
  "Please Provide more context for this."

---
Context:
{context}

Question: {question}
""",
input_variables=["context", "question"],
)


def query(question: str) -> str:
    """Query retriever + Gemini API and return response text."""
    try:
        # Retrieve relevant documents
        retrieved_docs = retriever.invoke(question)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # Final prompt
        final_prompt = prompt.invoke(
            {"context": context_text, "question": question}
        )

        # Gemini API call
        response = requests.post(
            GEMINI_API_URL + f"?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"role": "user", "parts": [{"text": str(final_prompt)}]}
                ],
                "generationConfig": {"maxOutputTokens": 1000},
            },
            timeout=60,
        )

        if response.status_code != 200:
            logger.error(f"Gemini API error: {response.status_code} {response.text}")
            return "Error Occurred."

        gemini_data = response.json()

        # Extract assistant reply
        text = (
            gemini_data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "No response")
        )

        return text.strip()

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return "Error Occurred."

