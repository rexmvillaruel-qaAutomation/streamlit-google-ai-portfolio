import streamlit as st
import time
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

# --- SIDEBAR PORTFOLIO PROFILE ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg", width=50)
    st.image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png", width=120)
    st.markdown("**Project:** 8 Courses, 1 Platform")
    st.markdown("**Powered by:** Google Gemini 3.8 Flash")
    st.markdown("---")
    st.markdown("### 👨‍💻 Created by")
    st.markdown("**Rex Melvin Villaruel**") 
    st.markdown("Software QA Automation Engineer")
    
    
#st.title("8 Courses, 1 Platform: A Google AI Professional Portfolio")
# --- MAIN PAGE TITLE NA MAY GOOGLE COLORS ---
st.markdown("""
<h1 style='text-align: center; font-weight: bold;'>
    8 Courses, 1 Platform:<br> 
    A <span style='color: #4285F4;'>G</span><span style='color: #EA4335;'>o</span><span style='color: #FBBC05;'>o</span><span style='color: #4285F4;'>g</span><span style='color: #34A853;'>l</span><span style='color: #EA4335;'>e</span> AI Professional Portfolio
</h1>
<hr>
""", unsafe_allow_html=True)

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

    st.warning("🛡️ **Data Privacy Warning:** This is a portfolio project using a free-tier AI API. Please do not upload confidential or internal company documents. Use dummy or public files only.")
    
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
                    # Error Handling
                       # st.error(f"API Error Details: {e}")
                        st.warning("We're experiencing high traffic with the AI server right now. Please try again in a few moments.")
        else:
                st.warning("Please enter a question first.")


# Phase 4: Tab 3 - Wellness Guardrails
with tab3:
    st.header("🧘‍♂️ Wellness Guardrails")
    st.write("AI-powered burnout prevention and work-life balance advice tailored for working professionals.")
    st.divider()

    # Interactive Inputs para sa assessment
    col1, col2 = st.columns(2)
    with col1:
        hours_worked = st.slider("Hours spent working today:", min_value=0, max_value=16, value=8)
    with col2:
        stress_level = st.select_slider("Current Stress Level:", options=["Chill", "Manageable", "High", "Burnout Risk"])

    focus_area = st.multiselect(
        "Any specific physical/mental strain?", 
        ["Eye Strain", "Back/Neck Pain", "Mental Fatigue", "Sleepiness", "Headache"],
        default=["Eye Strain"]
    )

    if st.button("Generate Wellness Routine"):
        with st.spinner("Consulting your AI Wellness Coach..."):
            
            prompt = f"""
            Act as an occupational health coach for software engineers.
            Hours worked: {hours_worked}. Stress level: '{stress_level}'. 
            Strain: {', '.join(focus_area)}.
            
            Provide EXACTLY 3 extremely short, actionable bullet points for immediate recovery.
            Rule 1: No introductions.
            Rule 2: No conclusions.
            Rule 3: Maximum of 50 words total.
            """
            
            # Auto-Retry Logic (Maximum 3 attempts)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response_stream = client.models.generate_content_stream(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    
                    st.write_stream(chunk.text for chunk in response_stream if chunk.text)
                    break
                    
                except Exception as e:
                    if "503" in str(e) and attempt < max_retries - 1:
                        time.sleep(2)
                        continue 
                    else:
                        #st.error(f"API Error: {e}")
                        st.warning("The AI server is extremely busy right now after multiple attempts. Quick tip: Stand up, stretch your back, and drink a glass of water!")
                        break

# Phase 5: Tab 4 - Routine Analytics (Interactive)
with tab4:
    st.header("📊 Routine Analytics")
    st.write("Adjust the sliders to simulate your hours today and see how it impacts your weekly productivity trends in real-time.")
    st.divider()

    # --- INTERACTIVE SLIDERS ---
    st.markdown("### 🎛️ Log Today's Hours")
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        today_deep = st.slider("Deep Work (hrs)", min_value=0, max_value=12, value=4)
    with col_in2:
        today_meet = st.slider("Meetings (hrs)", min_value=0, max_value=8, value=2)
    with col_in3:
        today_admin = st.slider("Admin/Emails (hrs)", min_value=0, max_value=6, value=2)

    st.write("") # Spacer

    # --- DYNAMIC CALCULATIONS ---
    total_today = today_deep + today_meet + today_admin
    # Computation para sa focus score: (Deep Work / Total Hours) * 100
    focus_score = int((today_deep / total_today) * 100) if total_today > 0 else 0
    target_score = 60 # Target focus percentage
    delta_score = focus_score - target_score

    # --- TOP METRICS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Today's Deep Work", value=f"{today_deep} hrs")
    with col2:
        st.metric(label="Total Hours Logged", value=f"{total_today} hrs")
    with col3:
        st.metric(label="Daily Focus Score", value=f"{focus_score}%", delta=f"{delta_score}% vs Target")

    st.write("") # Spacer

    # --- BAR CHART: DYNAMIC TIME ALLOCATION ---
    st.markdown("### 📅 Weekly Time Allocation")
    st.caption("Real-time breakdown of your time. Notice how the 'Today' column updates as you move the sliders.")
    
    # Gumagamit tayo ng dynamic variables (today_deep, today_meet, today_admin) imbes na hardcoded numbers
    time_data = pd.DataFrame(
        {
            "Deep Work (Focus)": [4, 5, 3, 6, today_deep],
            "Meetings (Collab)": [3, 2, 4, 1, today_meet],
            "Admin (Emails/Routines)": [1, 1, 1, 1, today_admin]
        },
        index=["Mon", "Tue", "Wed", "Thu", "Today"]
    )
    st.bar_chart(time_data)

    # --- LINE CHART: DYNAMIC ENERGY LEVELS ---
    st.markdown("### ⚡ Daily Energy & Focus Trends")
    
    # Dynamic logic: Bumababa ang energy kapag maraming meeting/admin, tumataas kapag deep work
    dynamic_energy = max(10, 100 - (today_meet * 8) - (today_admin * 5) + (today_deep * 2))
    if dynamic_energy > 100: dynamic_energy = 100

    energy_data = pd.DataFrame(
        {
            "Energy Level (%)": [75, 90, 65, 85, dynamic_energy]
        },
        index=["Mon", "Tue", "Wed", "Thu", "Today"]
    )
    st.line_chart(energy_data)