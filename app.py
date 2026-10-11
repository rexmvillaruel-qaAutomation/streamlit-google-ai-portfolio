import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables (kukunin nito ang nasa .env file)
load_dotenv()

# Page setup
st.set_page_config(page_title="8 Courses, 1 Platform", layout="wide")

st.title("8 Courses, 1 Platform: A Google AI Professional Portfolio")

st.sidebar.title("Navigation")
st.sidebar.write("Dito natin ilalagay ang 4 modules mamaya.")

st.write("Kung nakikita mo ito, gumagana nang maayos ang Streamlit at handa na tayo mag-integrate ng Gemini API!")