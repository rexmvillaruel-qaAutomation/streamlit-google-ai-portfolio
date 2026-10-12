# 8 Courses, 1 Platform: A Google AI Professional Portfolio 🚀

## Project Overview
A unified Streamlit web application showcasing practical implementations of the Google AI Professional Certificate. This platform serves as an AI-powered Daily Routine Manager, applying generative AI concepts, LLM APIs, responsible AI practices, and data pipelines to optimize working memory and daily tasks.

**Created by:** Rex Melvin Villaruel | Software QA Automation Engineer

---

## 💡 Project Origin & Inspiration: The "Why" Behind the Platform
This project was born out of a desire to translate the theoretical knowledge from the **Google AI Professional Certificate** into a tangible, practical tool. Instead of building isolated mini-projects for each of the 8 courses, I challenged myself to consolidate everything I learned into a single, unified platform. 

As a Software QA Automation Engineer, my day-to-day involves constant context-switching, analyzing extensive documentation, and managing complex test executions. I realized I needed a personalized AI assistant that could address these specific challenges. I conceptualized this platform to optimize cognitive load, streamline information retrieval, and promote sustainable work habits.

---

## 🧠 Core Concepts & Methodologies Applied
This platform isn't just about writing code; it's about integrating powerful frameworks and methodologies I've studied and explored:

1. **The Four-Chunk Working Memory Framework:** Applied directly to the Task Organizer (Tab 1). Based on the psychological concept of working memory limits, the AI processes daily dumps of tasks and structures them into strictly 4 optimal time blocks to prevent cognitive overload and burnout.
2. **Retrieval-Augmented Generation (RAG):** Applied in the Smart Context Q&A (Tab 2). Inspired by my explorations into using LangChain and local AI setups for automating Playwright test log analysis and test scenario generation. This feature restricts the AI to answer *only* based on the uploaded contextual documents (PDF, Word, Excel), ensuring zero hallucination.
3. **The QA Automation Mindset (Stable over Flaky):** As an automation engineer, I treat UI development like test scripting. I prioritized stable CSS selectors (using `data-baseweb` attributes instead of dynamic classes) and avoided "flaky" design hacks (like forced sticky headers that cause overlapping overlays) to ensure a robust, cross-platform user experience.

---

## 🌟 Features (The 4 Main Tabs)
1. **4-Chunk Task Organizer:** An AI-driven task scheduler that optimizes daily workload into 4 manageable time blocks.
2. **Smart Context Q&A (RAG):** Upload dummy documents and ask context-specific questions powered by Gemini 3.8 Flash.
3. **Wellness Guardrails:** An interactive module with dynamic sliders and strain selection to generate quick, AI-powered physical and mental recovery routines.
4. **Routine Analytics:** A real-time dashboard with dynamic sliders that simulate workday hours and update performance metrics instantly.

---

## 🗺️ Development Roadmap & Phases
To ensure stability and a professional user experience, this platform was developed in three structured phases:

* **✅ Phase 1: Core Architecture & Logic:** Built the foundational 4-tab structure, integrated the Gemini API for RAG and task generation, and developed the dynamic logic for real-time slider metrics.
* **✅ Phase 2: UI/UX Polish & Google Aesthetic:** Overrode Streamlit's default CSS to implement a minimalist, Google-inspired design. Centered tabs, established visual hierarchy, refined sidebar elements, and added a subtle gradient background.
* **🚀 Phase 3: Final QA, UAT, & Deployment (Current):** End-to-end testing across different screen sizes, addressing layout bugs, finalizing technical documentation, and deploying the application to a live production environment.

---

## 🛠️ Tech Stack
- **Frontend/UI:** Streamlit, Custom HTML/CSS
- **AI/LLM:** Google Gemini Pro API (`google-genai`)
- **Data Processing:** Pandas, PyPDF
- **Language:** Python 3.11

---

## 🐞 The QA Diary: Development Journey & Troubleshooting
Here are the key challenges, investigations, and fixes implemented during the development of this platform:

### 1. The "Flaky" Streamlit Tab CSS Overrides
* **Issue:** Streamlit's default tab design didn't fit the desired Google Material aesthetic. Standard HTML tag targeting failed because Streamlit dynamically changes class names.
* **Resolution:** Used deep wildcard selectors and specific data attributes (`[data-baseweb="tab"] *`) to forcefully apply `#1A73E8` (Google Blue) for active states, `font-weight: 500` for inactive tabs, and `justify-content: center`.

### 2. The Sticky Header "Floating Overlay" Bug
* **Issue:** Attempted to implement a "Sticky Header" using `position: fixed` to keep the main title visible while scrolling. 
* **Investigation:** The title was removed from the normal document flow, causing the tabs and User Guide to overlap and visually clash with the title text when scrolling.
* **QA Decision & Fix:** Prioritized UI stability over flashy CSS hacks. Dropped the sticky header feature to ensure the dashboard remains fully readable.

### 3. Typography and Visual Hierarchy Refinement
* **Issue:** Default `st.header()` tags created massive titles inside the tabs, making the interface look cluttered. 
* **Resolution:** Downgraded tab titles to `st.subheader()` for a cleaner look. Added a global subtle linear gradient (`#FFFFFF` to `#F1F3F4`).

### 4. Sidebar Rendering Errors (Broken Image & Raw HTML)
* **Issue:** The custom sidebar design showed a broken image icon for the Gemini logo, and the Streamlit engine rendered raw HTML tags as plain text inside a white code block.
* **Resolution:** Replaced the broken external image link with a stable `✨` emoji. Removed all structural indentations inside the HTML triple-quotes.

---

## 💻 Local Setup
1. Clone this repository.
2. Install dependencies: 
   ```bash
   pip install streamlit google-genai python-dotenv pandas pypdf