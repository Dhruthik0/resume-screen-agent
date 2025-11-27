import pdfminer.high_level
from docx import Document
import re
import os
from utils import extract_skills_from_text


# ------------------------
# TEXT EXTRACTORS
# ------------------------

def extract_text_from_pdf(bytes_data):
    """Extract text from a PDF file."""
    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(bytes_data)

    try:
        text = pdfminer.high_level.extract_text(temp_path)
    except:
        text = ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


def extract_text_from_docx(bytes_data):
    """Extract text from a DOCX file."""
    temp_path = "temp.docx"
    with open(temp_path, "wb") as f:
        f.write(bytes_data)

    try:
        doc = Document(temp_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except:
        text = ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


def extract_text_from_txt(bytes_data):
    """Extract text from TXT file."""
    try:
        return bytes_data.decode("utf-8", errors="ignore")
    except:
        return ""


# ------------------------
# MAIN PARSER
# ------------------------

def parse_resume(uploaded_file):
    """Auto-detect file type and extract information."""
    
    file_name = uploaded_file.name.lower()
    raw = uploaded_file.read()

    # Detect extension
    if file_name.endswith(".pdf"):
        text = extract_text_from_pdf(raw)

    elif file_name.endswith(".docx"):
        text = extract_text_from_docx(raw)

    elif file_name.endswith(".txt"):
        text = extract_text_from_txt(raw)

    else:
        return {
            "error": f"Unsupported file type: {file_name}. Upload PDF, DOCX, or TXT."
        }

    # Extract email
    email = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email[0] if email else None

    # Extract skills
    skills = extract_skills_from_text(text)

    # Extract experience
    exp = extract_experience(text)

    return {
        "file_name": file_name,
        "email": email,
        "text": text,
        "skills": skills,
        "total_experience": exp
    }


# ------------------------
# EXPERIENCE EXTRACTION
# ------------------------

def extract_experience(text):
    """
    Finds years of experience in text (e.g., '3 years', '5+ years').
    Returns float or None.
    """
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    if matches:
        try:
            return float(matches[0])
        except:
            return None
    return None
