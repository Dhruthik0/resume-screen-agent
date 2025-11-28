def get_explanation(jd, candidate, score):
    name = candidate.get("name") or candidate.get("file_name") or "Candidate"
    skills = candidate.get("skills", [])
    exp = candidate.get("total_experience")

    parts = []
    parts.append(f"{name} has a score of {score:.1f} based on skill, experience, and JD similarity.")

    if skills:
        parts.append(f"Key skills found: {', '.join(skills[:8])}.")
    if exp is not None:
        parts.append(f"Reported experience: {exp} years.")

    parts.append("This is a heuristic explanation generated without an LLM.")
    return " ".join(parts)


def get_questions(jd, candidate):
    return (
        "- Can you walk me through a recent project that closely matches this job description?\n"
        "- Which of your skills do you think are the strongest fit for this role, and why?\n"
        "- Tell me about a challenge you faced in a previous role and how you handled it."
    )
