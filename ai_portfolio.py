import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Page setup
st.set_page_config(page_title="8 Courses, 1 Platform", layout="wide")
st.title("8 Courses, 1 Platform: A Google AI Professional Portfolio")

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
    
    # Input area for the user
    user_tasks = st.text_area("Enter your tasks here (e.g., QA testing, API scripts, gym session, meetings):", height=150)
    
    if st.button("Organize Tasks"):
        if user_tasks:
            with st.spinner("AI is organizing your schedule..."):
                # System Prompt Engineering
                prompt = f"""
                You are an expert productivity coach. Group the following tasks into 4 distinct time chunks:
                1. Morning Focus (High energy tasks)
                2. Mid-day Momentum (Collaborative or routine tasks)
                3. Afternoon Wrap-up (Admin and closing tasks)
                4. Evening Wind-down (Personal, health, and relaxation)
                
                Format the output cleanly using markdown. Here are the tasks: 
                {user_tasks}
                """
                
                # Call Gemini API
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # Display output
                st.markdown(response.text)
        else:
            st.warning("Please enter tasks in the text box before clicking the button.")