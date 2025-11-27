# app/parser.py

import re
import os
from typing import Dict

# ------------------------
# Optional imports
# ------------------------

# Try pdfminer
try:
    import pdfminer.high_level as pdf_high_level
    HAS_PDFMINER = True
except ImportError:
    pdf_high_level = None
    HAS_PDFMINER = False

# Try python-docx
try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    Document = None
    HAS_DOCX = False

from utils import extract_skills_from_text


# ------------------------
# TEXT EXTRACTORS
# ------------------------

def extract_text_from_pdf(bytes_data: bytes) -> str:
    """Extract text from a PDF file if pdfminer is available."""
    if not HAS_PDFMINER:
        # No pdfminer in this environment (e.g. Streamlit Cloud)
        return ""

    temp_path = "temp.pdf"
    with open(temp_path, "wb") as f:
        f.write(bytes_data)

    try:
        text = pdf_high_level.extract_text(temp_path) or ""
    except Exception:
        text = ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


def extract_text_from_docx(bytes_data: bytes) -> str:
    """Extract text from a DOCX file if python-docx is available."""
    if not HAS_DOCX:
        # No python-docx in this environment
        return ""

    temp_path = "temp.docx"
    with open(temp_path, "wb") as f:
        f.write(bytes_data)

    try:
        doc = Document(temp_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        text = ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


def extract_text_from_txt(bytes_data: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return bytes_data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


# ------------------------
# EXPERIENCE EXTRACTION
# ------------------------

def extract_experience(text: str):
    """
    Finds years of experience in text (e.g., '3 years', '5+ years').
    Returns float or None.
    """
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            return None
    return None


# ------------------------
# MAIN PARSER
# ------------------------

def parse_resume(uploaded_file) -> Dict:
    """Auto-detect file type and extract information."""
    file_name = uploaded_file.name
    file_name_lower = file_name.lower()
    raw = uploaded_file.read()

    # Detect extension
    if file_name_lower.endswith(".pdf"):
        text = extract_text_from_pdf(raw)
        if not text and not HAS_PDFMINER:
            text = (
                "PDF parsing is not available in this deployment. "
                "Please upload a DOCX or TXT version of the resume."
            )

    elif file_name_lower.endswith(".docx"):
        text = extract_text_from_docx(raw)
        if not text and not HAS_DOCX:
            text = (
                "DOCX parsing is not available in this deployment. "
                "Please upload a TXT version of the resume."
            )

    elif file_name_lower.endswith(".txt"):
        text = extract_text_from_txt(raw)

    else:
        text = f"Unsupported file type: {file_name}. Upload PDF, DOCX, or TXT."

    # Extract email
    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = emails[0] if emails else None

    # Extract skills
    skills = extract_skills_from_text(text)

    # Extract experience
    exp = extract_experience(text)

    return {
        "file_name": file_name,
        "email": email,
        "text": text,
        "skills": skills,
        "total_experience": exp,
    }
