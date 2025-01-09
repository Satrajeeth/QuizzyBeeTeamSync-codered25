from flask import Flask, request, jsonify, send_from_directory
import os
import pdfplumber
import docx
from fpdf import FPDF
import google.generativeai as genai

# Flask App Configuration
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
RESULTS_FOLDER = 'results/'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

# Ensure folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

# API Configuration
os.environ["GOOGLE_API_KEY"] = 'AIzaSyDKiAwKDDES5wq7upu3wHwEkW8PEkrscgA'  # Add your API Key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Utility Functions
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

def question_mcqs_generator(input_text, num_questions):
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

# Flask Routes
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/generate_mcqs', methods=['POST'])
def generate_mcqs():
    data = request.json
    file_path = data.get('file_path')
    num_questions = data.get('num_questions', 5)

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "Invalid or missing file path"}), 400

    text = extract_text_from_file(file_path)
    if not text:
        return jsonify({"error": "Unable to extract text from the file"}), 400

    mcqs = question_mcqs_generator(text, num_questions)
    text_filename = f"mcqs_{os.path.basename(file_path)}.txt"
    pdf_filename = f"mcqs_{os.path.basename(file_path)}.pdf"

    text_path = save_mcqs_to_file(mcqs, text_filename)
    pdf_path = create_pdf(mcqs, pdf_filename)

    return jsonify({"message": "MCQs generated successfully", "text_file": text_path, "pdf_file": pdf_path}), 200

@app.route('/results/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(RESULTS_FOLDER, filename)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
