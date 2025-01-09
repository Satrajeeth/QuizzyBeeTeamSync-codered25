import os
import streamlit as st
import pdfplumber
import docx
from fpdf import FPDF
from pathlib import Path
import time

# API configuration
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = 'AIzaSyC5LikCrTBzP3F6XR-cks7vUl27c_5FZ7U'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'results/'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text
    elif ext == 'docx':
        doc = docx.Document(file_path)
        text = ' '.join([para.text for para in doc.paragraphs])
        return text
    elif ext == 'txt':
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read()
    return None

def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    ---
    {input_text}
    ---
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt)
    if response and hasattr(response, "text"):
        return response.text.strip()
    else:
        return "Failed to generate MCQs. Please try again."

def Short_notes_generator(input_text, num_notes):
    prompt = f"""
    You are an AI assistant helping the user generate concise and meaningful short notes based on the following text:
    ---
    {input_text}
    ---
    Please generate {num_notes} short notes. Each note should be concise, clear, and summarize key points from the text.
    Format:
    ## Note [index]
    [Short Note]
    """
    response = model.generate_content(prompt)
    if response and hasattr(response, "text"):
        return response.text.strip()
    else:
        return "Failed to generate short notes. Please try again."

def save_to_file(content, filename):
    results_path = os.path.join(RESULTS_FOLDER, filename)
    with open(results_path, 'w') as f:
        f.write(content)
    return results_path

def create_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section in content.split("##"):
        if section.strip():
            pdf.multi_cell(0, 10, section.strip())
            pdf.ln(5)

    pdf_path = os.path.join(RESULTS_FOLDER, filename)
    pdf.output(pdf_path)
    return pdf_path

def pomodoro_timer(minutes, seconds):
    placeholder = st.sidebar.empty()

    # Display only the timer in the sidebar
    with placeholder.container():
        st.markdown("""
        <div style="border: 2px solid #4CAF50; padding: 10px; text-align: center; background-color: #ffffff;">
        <h3 style="color: #4CAF50;">Focus Mode Timer</h3>
        <p style="font-size: 32px; font-weight: bold; color: #000000;" id="timer">00:00</p>
        </div>
        """, unsafe_allow_html=True)

    # Start the countdown
    while minutes >= 0:
        time.sleep(1)  # Delay for one second
        if seconds == 0:
            if minutes == 0:
                break
            minutes -= 1
            seconds = 59
        else:
            seconds -= 1

        # Update the timer display
        placeholder.markdown(f"""
        <div style="border: 2px solid #4CAF50; padding: 10px; text-align: center; background-color: #ffffff;">
        <h3 style="color: #4CAF50;">Focus Mode Timer</h3>
        <p style="font-size: 32px; font-weight: bold; color: #000000;">{minutes:02}:{seconds:02}</p>
        </div>
        """, unsafe_allow_html=True)

    # Display time's up message
    placeholder.markdown("""
    <div style="border: 2px solid #4CAF50; padding: 10px; text-align: center; background-color: #ffffff;">
    <h3 style="color: #4CAF50;">Focus Mode Timer</h3>
    <p style="font-size: 24px; font-weight: bold; color: red;">Time's Up! Take a break.</p>
    </div>
    """, unsafe_allow_html=True)

st.title("QuizzyBee")
st.write("Upload a file and generate multiple-choice questions (MCQs) or short notes automatically!")

uploaded_file = st.file_uploader("Upload your document (PDF, TXT, DOCX):", type=['pdf', 'txt', 'docx'])

generation_type = st.radio("What do you want to generate?", ("MCQs", "Short Notes"))

num_items = st.slider("How many items do you want?", min_value=1, max_value=20, value=5, step=1)

focus_mode = st.checkbox("Enable Focus Mode")

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text_from_file(file_path)

    if text:
        with st.spinner(f"Generating {generation_type}..."):
            if generation_type == "MCQs":
                content = Question_mcqs_generator(text, num_items)
            else:
                content = Short_notes_generator(text, num_items)

            txt_filename = f"generated_{generation_type.lower()}_{uploaded_file.name.rsplit('.', 1)[0]}.txt"
            pdf_filename = f"generated_{generation_type.lower()}_{uploaded_file.name.rsplit('.', 1)[0]}.pdf"

            save_to_file(content, txt_filename)
            create_pdf(content, pdf_filename)

            st.session_state.generated_content = content

        st.success(f"{generation_type} generated successfully!")

        # Display the generated content
        st.write(f"Here are the generated {generation_type}:")
        for section in content.split("##"):
            if section.strip():
                lines = section.strip().splitlines()
                for line in lines:
                    st.markdown(line)
                st.markdown("---")

        # Provide download options
        st.write("Download options:")
        st.download_button(label="Download as TXT",
                           data=open(os.path.join(RESULTS_FOLDER, txt_filename)).read(),
                           file_name=txt_filename)
        st.download_button(label="Download as PDF",
                           data=open(os.path.join(RESULTS_FOLDER, pdf_filename), 'rb').read(),
                           file_name=pdf_filename, mime='application/pdf')

        # Focus mode
        if focus_mode:
            minutes = st.sidebar.number_input("Set Timer Minutes", min_value=1, max_value=60, value=25, step=1)
            seconds = st.sidebar.number_input("Set Timer Seconds", min_value=0, max_value=59, value=0, step=1)
            st.sidebar.write("Focus Mode Enabled")
            pomodoro_timer(minutes, seconds)
