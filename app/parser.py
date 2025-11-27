import re
import os
from typing import Dict

try:
    import pdfminer.high_level as pdf_high_level
    HAS_PDFMINER = True
except ImportError:
    pdf_high_level = None
    HAS_PDFMINER = False

import docx2txt
from utils import extract_skills_from_text


def extract_text_from_pdf(bytes_data: bytes) -> str:
    if not HAS_PDFMINER:
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
    temp_path = "temp.docx"
    with open(temp_path, "wb") as f:
        f.write(bytes_data)

    try:
        text = docx2txt.process(temp_path) or ""
    except Exception:
        text = ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return text


def extract_text_from_txt(bytes_data: bytes) -> str:
    try:
        return bytes_data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def extract_experience(text: str):
    matches = re.findall(r"(\d+)\+?\s+years?", text.lower())
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            return None
    return None


def parse_resume(uploaded_file) -> Dict:
    file_name = uploaded_file.name
    file_name_lower = file_name.lower()
    raw = uploaded_file.read()

    if file_name_lower.endswith(".pdf"):
        text = extract_text_from_pdf(raw)
        if not text and not HAS_PDFMINER:
            text = (
                "PDF parsing is not available in this deployment. "
                "Please upload a DOCX or TXT version of the resume."
            )

    elif file_name_lower.endswith(".docx"):
        text = extract_text_from_docx(raw)
        if not text:
            text = (
                "DOCX parsing failed in this deployment. "
                "Please upload a TXT version of the resume."
            )

    elif file_name_lower.endswith(".txt"):
        text = extract_text_from_txt(raw)

    else:
        text = f"Unsupported file type: {file_name}. Upload PDF, DOCX, or TXT."

    emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = emails[0] if emails else None

    skills = extract_skills_from_text(text)
    exp = extract_experience(text)

    return {
        "file_name": file_name,
        "email": email,
        "text": text,
        "skills": skills,
        "total_experience": exp,
    }
