# 8 Courses, 1 Platform: A Google AI Professional Portfolio

## Project Overview
A unified Streamlit web application showcasing practical implementations of the Google AI Professional Certificate. This platform serves as an AI-powered Daily Routine Manager, applying generative AI concepts, LLM APIs, responsible AI practices, and data pipelines to optimize working memory and daily tasks.

## Tech Stack
* **Frontend/UI:** Streamlit
* **AI/LLM:** Google Gemini Pro API (`google-genai`)
* **Data Processing:** Pandas, PyPDF
* **Language:** Python 3.11

## Local Setup
1. Clone this repository.
2. Install dependencies: `pip install streamlit google-genai python-dotenv pandas pypdf`
3. Create a `.env` file in the root directory and add your API key:
   `GEMINI_API_KEY="your_api_key_here"`
4. Run the application: `streamlit run app.py`