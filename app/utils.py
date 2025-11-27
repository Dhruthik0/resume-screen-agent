def extract_skills_from_text(text):
    vocab = ["python","java","sql","excel","aws","react","node","tensorflow","pandas","numpy","spark"]
    text = text.lower()
    return [s for s in vocab if s in text]
