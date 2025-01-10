# <a name="mcq-generator"></a> QuizzyBee: Automatically Create Multiple-Choice Questions from Uploaded Text Documents

## Table of Contents
- [Code Overview and Breakdown](#code-overview-and-breakdown) 
- [Skills Acquired](#skills-acquired)
- [Technologies Used](#technologies-used)
- [How To Run the Code](#how-to-run-the-code)
- [Contributing](#contributing)

## <a name="detailed-breakdown"></a> Code Overview and Breakdown

This project is an AI-powered web application designed to generate multiple-choice questions (MCQs) from text documents, using Streamlit as the web interface and Google’s Gemini-1.5 Pro AI model for generating questions. Users can upload files (PDF, DOCX, or TXT), and the application extracts text from the document, processes it, and generates a specified number of MCQs with four answer options (A-D). The correct answer is also provided for each question.

The project is divided into several major segments:

1. **File Upload and Text Extraction**

This part allows users to upload files in multiple formats, including PDF, TXT, and DOCX. It extracts text from the files using libraries like pdfplumber (for PDF) and python-docx (for DOCX).

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/19.png?raw=true">

2. **MCQ Generation Using AI**

The Google Generative AI (Gemini model) is used to generate MCQs from the extracted text. The code sends a formatted prompt to the AI model, asking it to generate a specified number of questions.

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/20.png?raw=true">

3. **Displaying and Downloading MCQs**

Once the MCQs are generated, they are displayed on the webpage, and users can download them as either a TXT or PDF file. The PDF generation is handled using the FPDF library.

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/21.png?raw=true">

4. **Web Application Interface**

The user interface is built using Streamlit, which allows for interactive web apps in Python. Users can upload files, select the number of questions, and regenerate questions if needed. The results are displayed directly in the app.

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/22.png?raw=true">

## Skills Acquired:
* **Text Processing:** Handling text extraction from multiple file formats (PDF, DOCX, TXT).
* **API Integration:** Integrating Google’s Generative AI API for content generation.
* **Web Development with Streamlit:** Building interactive web apps with file uploads, user inputs, and downloadable results.
* **PDF Generation:** Utilizing FPDF to convert generated questions into a professional-looking PDF.
* **Error Handling:** Managing different file encodings and edge cases during text extraction.

## Technologies Used
* **Streamlit:** Used to create the web interface for uploading documents, interacting with users, and displaying MCQs.
* **pdfplumber:** A library for extracting text from PDF documents.
* **python-docx:** Extracts text from DOCX (Microsoft Word) files.
* **FPDF:** A lightweight library to generate PDF files.
* **Google Generative AI (Gemini Model):** This API is used to generate the actual MCQs from the text provided by the user.
* **OS Module:** Handles file paths and directory creation.

## How To Run the Code
To run the code on your local machine, follow these steps:

**Step 1: Clone the Repository and Install Requirements**

1. Clone the project repository or copy the code to your local machine.
2. Ensure you have Python installed.
3. Create a virtual environment (optional but recommended):

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/23.png?raw=true">

    Then, activate the virtual environment:
      **Windows:** env\Scripts\activate
      **Mac/Linux:** source env/bin/activate
      
4. Install the required Python libraries. If you have a requirements.txt file (as you do), you can install the dependencies directly:

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/24.png?raw=true">

**Step 2: Set up API Key**
The project requires an API key to access Google’s Generative AI model. You must set up your **Google API Key** and place it in your environment as follows:

1. Go to Google Cloud Console and generate an API key for the Gemini Model.
2. Update the code where the GOOGLE_API_KEY is required:

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/25.png?raw=true">

**Step 3: Run the Streamlit Application**
Once the environment is set up and dependencies are installed, run the Streamlit web app using the following command:

<img width="722" alt="MCQ-Generator" src="https://github.com/Dev-Godswill/picture-files/blob/main/26.png?raw=true">

Replace your_script_name.py with the name of the script that contains the code above.

**Step 4: Access the Web Interface**
After running the Streamlit app, a URL will be provided in your terminal (usually http://localhost:8501). Open this in your web browser to start using the MCQ generator.

**Step 5: Upload Files and Generate MCQs**
* Upload a text document in PDF, DOCX, TXT or image format
* Specify the number of questions you want to generate or the number of points.
* Download the MCQs as TXT or PDF files.
* Translation to Hindi available
* Focus Mode enabled


