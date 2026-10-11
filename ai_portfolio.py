import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
import pandas as pd
from pypdf import PdfReader
import docx
import pptx

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Page setup
st.set_page_config(page_title="8 Courses, 1 Platform", layout="wide")
st.title("8 Courses, 1 Platform: A Google AI Professional Portfolio")

# Setup session state for clearing inputs
if "reset_key" not in st.session_state:
    st.session_state.reset_key = 0

if "reset_key_tab1" not in st.session_state:
    st.session_state.reset_key_tab1 = 0

# Create 4 Tabs for the 4 modules
tab1, tab2, tab3, tab4 = st.tabs([
    "1: 4-Chunk Task Organizer", 
    "2: Smart Context Q&A", 
    "3: Wellness Guardrails", 
    "4: Routine Analytics"
])

# Phase 1: Tab 1 Development
with tab1:
    st.header("The 4-Chunk Task Organizer")
    st.write("Dump all your tasks for today, and the AI will organize them into 4 time blocks to help prevent burnout.")
    
# Bagong Clear Button para sa Tab 1
    if st.button("Clear / Reset Tasks"):
        st.session_state.reset_key_tab1 += 1
        st.rerun()

    # FIX 1: Nasa loob na ng parenthesis ang key
    user_tasks = st.text_area(
        "Enter your tasks here (e.g., QA testing, API scripts, gym session, meetings):", 
        height=150,
        key=f"task_input_{st.session_state.reset_key_tab1}"
    )
    
    if st.button("Organize Tasks"):
        if user_tasks:
            try:
                # Ibinalik natin ang nawalang prompt dito bago tawagin ang API!
                prompt = f"""
                You are an expert productivity coach. Group the following tasks into 4 distinct time chunks:
                1. Morning Focus (High energy tasks)
                2. Mid-day Momentum (Collaborative or routine tasks)
                3. Afternoon Wrap-up (Admin and closing tasks)
                4. Evening Wind-down (Personal, health, and relaxation)
                
                Format the output cleanly using markdown. Here are the tasks: 
                {user_tasks}
                """
                
                # Isang buong block para sabay ang loading indicator at typing effect
                with st.spinner("AI is organizing your schedule..."):
                    response_stream = client.models.generate_content_stream(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    
                    # Direct at mas malinis na Streamlit streaming generator
                    st.write_stream(chunk.text for chunk in response_stream if chunk.text)
                    
            except Exception as e:
                st.error("We're experiencing high traffic with the AI server right now. Please try again in a few moments.") 

        else:
            st.warning("Please enter tasks in the text box before clicking the button.")

# Phase 2: Tab 2 Development

# Extracting files

def extract_text(file):
    file_name = file.name
    extracted_text = ""
    
    try:
        if file_name.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
                    
        elif file_name.endswith(".docx"):
            doc = docx.Document(file)
            for para in doc.paragraphs:
                extracted_text += para.text + "\n"
                
        elif file_name.endswith(".pptx"):
            ppt = pptx.Presentation(file)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        extracted_text += shape.text + "\n"
                        
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file)
            extracted_text = df.to_string() 
            
    except Exception as e:
        # Kapag corrupted ang file, ito ang ire-return niya imbes na mag-crash
        st.error(f"⚠️ Warning: Could not read {file_name}. The file might be corrupted.")
        return f"--- ERROR: {file_name} is corrupted and could not be read. ---\n"
        
    return extracted_text

with tab2:
    st.header("Smart Context Q&A")
    st.write("Upload your documents (PDF, Word, Excel, PPT) and ask the AI questions about them.")

# Reset user input
    if st.button("Clear / Reset Data"):
        st.session_state.reset_key += 1
        st.rerun()

# Uploading files

    uploaded_files = st.file_uploader(
        "Upload data", 
        accept_multiple_files=True, 
        type=["pdf", "docx", "pptx", "xlsx"],
        key=f"uploader_{st.session_state.reset_key}" # <-- Bagong linyang idinagdag
    )    

    if uploaded_files:
        st.success("Files uploaded successfully!")
        
      # 1. Pagsama-samahin ang text na may kasamang File Name labels. The answer of AI is categorized by the document
        all_document_text = ""
        for file in uploaded_files:
            all_document_text += f"--- START OF DOCUMENT: {file.name} ---\n"
            all_document_text += extract_text(file) + "\n"
            all_document_text += f"--- END OF DOCUMENT: {file.name} ---\n\n"
            
        # 2. UI para sa pagtatanong
        user_question = st.text_input(
            "Ask a question about the uploaded documents:",
                key=f"question_{st.session_state.reset_key}" # <-- Bagong linyang idinagdag
        )
        
        if st.button("Ask AI"):
            if user_question:
                with st.spinner("AI is analyzing your documents..."):
                    
                    prompt = f"""
                    You are a highly capable analytical assistant. Your task is to answer the user's question based strictly on the provided document text.
                    
                    DOCUMENT TEXT:
                    {all_document_text}

                    USER QUESTION:
                    {user_question}

                    INSTRUCTIONS:
                    1. Answer the question directly and concisely. Avoid flowery language.
                    2. Base your answer SOLELY on the Document Text provided above.
                    3. FORMATTING RULE: You MUST categorize your answer per document. Use the exact file name (e.g., **English.pdf**) as a header before presenting the answer derived from that specific document.
                    4. If the answer cannot be found within a specific document, explicitly state "Information not found in this document" under its respective header.
                    """
                
                    # Call Gemini API
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt,
                        )
                        st.markdown(response.text)
                    except Exception as e:
                      
                        st.error("We're experiencing high traffic with the AI server right now. Please try again in a few moments.")
        else:
                st.warning("Please enter a question first.")

    