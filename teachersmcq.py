import os
import streamlit as st
import pdfplumber
import docx
from fpdf import FPDF

# API configuration
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = 'AIzaSyDKiAwKDDES5wq7upu3wHwEkW8PEkrscgA'  # Add your API Key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

# File handling configuration
UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'results/'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}

# Ensure folders exist
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
            with open(file_path, 'r', encoding='utf-8') as file:  # Try UTF-8 first
                return file.read()
        except UnicodeDecodeError:
            # If it fails, try with a different encoding (ISO-8859-1 or Latin-1)
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read()
    return None

def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
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
    response = model.generate_content(prompt).text.strip()
    return response

def save_mcqs_to_file(mcqs, filename):
    results_path = os.path.join(RESULTS_FOLDER, filename)
    with open(results_path, 'w') as f:
        f.write(mcqs)
    return results_path

def create_pdf(mcqs, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for mcq in mcqs.split("## MCQ"):
        if mcq.strip():
            pdf.multi_cell(0, 10, mcq.strip())
            pdf.ln(5)  # Add a line break

    pdf_path = os.path.join(RESULTS_FOLDER, filename)
    pdf.output(pdf_path)
    return pdf_path

# Streamlit interface
st.title("MCQ Generator")
st.write("Upload a file and generate multiple-choice questions (MCQs) automatically!")

# File upload section
uploaded_file = st.file_uploader("Upload your document (PDF, TXT, DOCX):", type=['pdf', 'txt', 'docx'])

# Slider for selecting the number of questions
num_questions = st.slider("How many questions do you want?", min_value=1, max_value=20, value=5, step=1)

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Extract text and generate MCQs
    text = extract_text_from_file(file_path)

    if text:
        if 'mcqs' not in st.session_state:
            with st.spinner("Generating MCQs..."):
                mcqs = Question_mcqs_generator(text, num_questions)

                # Save MCQs as a file (optional)
                st.session_state.txt_filename = f"generated_mcqs_{uploaded_file.name.rsplit('.', 1)[0]}.txt"
                st.session_state.pdf_filename = f"generated_mcqs_{uploaded_file.name.rsplit('.', 1)[0]}.pdf"
                save_mcqs_to_file(mcqs, st.session_state.txt_filename)
                create_pdf(mcqs, st.session_state.pdf_filename)

                st.session_state.mcqs = mcqs
                st.session_state.uploaded_file_name = uploaded_file.name
                st.success("MCQs generated successfully!")

        else:
            mcqs = st.session_state.mcqs  # Retrieve previously generated MCQs

        # Display generated MCQs
        st.write("Here are the generated MCQs:")

        # Safeguard splitting logic for MCQs
        for mcq in mcqs.split("## MCQ"):
            if mcq.strip():  # Check if the mcq is not just empty or whitespace
                try:
                    question = mcq.split('A)')[0].strip()
                    option_a = mcq.split('A)')[1].split('B)')[0].strip()
                    option_b = mcq.split('B)')[1].split('C)')[0].strip()
                    option_c = mcq.split('C)')[1].split('D)')[0].strip()
                    option_d = mcq.split('D)')[1].split('Correct Answer:')[0].strip()
                    correct_answer = mcq.split('Correct Answer:')[1].strip()

                    # Display question and options
                    st.markdown(f"**{question}**")
                    st.write(f"A) {option_a}")
                    st.write(f"B) {option_b}")
                    st.write(f"C) {option_c}")
                    st.write(f"D) {option_d}")
                    st.markdown(f"**Correct Answer:** {correct_answer}")
                    st.markdown("---")

                except (IndexError, ValueError) as e:
                    st.error(f"Error processing MCQ: {mcq}. Skipping this question.")
                    continue

        # Button to regenerate questions
        if st.button("Regenerate MCQs"):
            with st.spinner("Generating new MCQs..."):
                mcqs = Question_mcqs_generator(text, num_questions)

                # Save MCQs as a file (optional)
                save_mcqs_to_file(mcqs, st.session_state.txt_filename)
                create_pdf(mcqs, st.session_state.pdf_filename)

                st.session_state.mcqs = mcqs
                st.success("New MCQs generated successfully!")

        # Option to download generated MCQs
        st.write("Download options:")
        st.download_button(label="Download as TXT",
                           data=open(os.path.join(RESULTS_FOLDER, st.session_state.txt_filename)).read(),
                           file_name=st.session_state.txt_filename)
        st.download_button(label="Download as PDF",
                           data=open(os.path.join(RESULTS_FOLDER, st.session_state.pdf_filename), 'rb').read(),
                           file_name=st.session_state.pdf_filename, mime='application/pdf')