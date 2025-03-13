import streamlit as st
import google.generativeai as genai
import json
import io
import docx
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
import os, re
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')



def extract_text_from_pdf(pdf_file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    for page in PDFPage.get_pages(pdf_file, caching=True, check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()

    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def parse_resume_details_with_gemini(resume_text):
    """Parses resume details using Gemini and returns them as a JSON object."""

    prompt = f"""
    Parse the following resume text and extract the following details:
    - Name
    - Email
    - Phone Number
    - Skills (list)
    - Education (list)
    - projects (list of objects, each with Title, Description)

    Return the details in JSON format, without any markdown formatting or code blocks.
    Do not include any extra text outside of the json.

    Resume Text:
    {resume_text}
    """

    try:
        response = model.generate_content(prompt)
        json_string = response.text

        # Remove markdown code block if present
        json_string = re.sub(r'```json\s*', '', json_string, count=1)
        json_string = re.sub(r'```\s*$', '', json_string, count=1)

        try:
            resume_data = json.loads(json_string)
            return resume_data
        except json.JSONDecodeError:
            st.error(f"Error: Gemini returned invalid JSON.\nRaw response: {json_string}")
            return None

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def generate_career_advice(resume_details):
    """Generates career advice using Gemini API."""

    if resume_details is None:
        return "Resume details could not be extracted."

    prompt = f"""
    Resume Details:
    {json.dumps(resume_details, indent=4)}

    Provide personalized career advice based on these details.
    Focus on potential career paths, Resume & Cover Letter Optimizationskill development, and job search strategies,Staying Updated with Industry Trendcs.
    instuctions:
      -persona:carrier advisor
      -audience:students
      -tone:encouraging
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Resume-Based Career Advisor")

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    file_type = uploaded_file.type

    if file_type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    resume_details = parse_resume_details_with_gemini(resume_text)

    if resume_details:
        st.subheader("Extracted Resume Details (JSON):")
        st.json(resume_details)

        if st.button("Get Career Advice"):
            career_advice = generate_career_advice(resume_details)
            st.subheader("Career Advice:")
            st.write(career_advice)
    else:
        st.write("Could not parse resume details.")

else:
    st.write("Please upload your resume to get personalized career advice.")