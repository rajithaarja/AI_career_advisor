# Resume-Based Career Advisor

This Streamlit application provides personalized career advice based on uploaded resumes. It leverages the Gemini API to extract resume details and generate tailored recommendations.

## Features

* **Resume Upload:** Supports PDF and DOCX file formats.
* **Resume Parsing:** Uses Gemini to extract key information from resumes, including:
    * Name
    * Email
    * Phone Number
    * Skills
    * Education
    * Experience
* **JSON Output:** Displays the extracted resume details in JSON format for easy verification.
* **Personalized Career Advice:** Generates career advice based on the extracted resume details, focusing on:
    * Potential career paths
    * Skill development
    * Job search strategies
* **Streamlit UI:** Provides a user-friendly interface for uploading resumes and viewing results.

## Prerequisites

* Python 3.6+
* A Google Cloud project with the Gemini API enabled.
* A Gemini API key.

## Installation

1.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a .env file:**

    * Create a .env in the code files and keep your gemini API key in it

## Usage

1.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```


2.  **Upload your resume:**

    * Click the "Browse files" button and select your resume file (PDF or DOCX).

3.  **View extracted resume details:**

    * The application will display the extracted resume details in JSON format.

4.  **Get career advice:**

    * Click the "Get Career Advice" button to generate personalized recommendations.

5.  **View career advice:**

    * The generated career advice will be displayed below the button.

## Requirements

* `streamlit`
* `google-generativeai`
* `pdfminer.six`
* `python-docx`

## Notes

* Ensure that your Gemini API key is properly configured in the `.env` file.
* The accuracy of the extracted resume details and career advice depends on the quality of the resume and the capabilities of the Gemini API.
* The prompt sent to gemini is crafted to remove any markdown that gemini might add to the json output.