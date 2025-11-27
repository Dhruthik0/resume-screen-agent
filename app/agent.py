# app/agent.py

from typing import List, Dict, Optional


# =========================
# 🔹 JD ANALYZER (AGENT THINKING STAGE 1)
# =========================
def analyze_jd(jd_text: str,
               required_skills: List[str],
               required_years: Optional[float]) -> Dict:
    """
    Agent checks JD quality & missing info
    """
    issues = []
    questions = []

    # Check if JD is too short
    if not jd_text or len(jd_text.strip()) < 30:
        issues.append("Job description is very short. Add more context about responsibilities and required skills.")

    # Check if skills missing
    if not required_skills or all(not s.strip() for s in required_skills):
        issues.append("Required skills are missing or empty.")
        questions.append("What are the must-have skills for this role? (3–5 keywords)")

    # Check experience requirement
    if not required_years or required_years <= 0:
        issues.append("Required experience not specified.")
        questions.append("How many years of experience is expected?")

    return {
        "issues": issues,
        "questions": questions
    }


# =========================
# 🔹 CANDIDATE CLASSIFICATION (AGENT THINKING STAGE 2)
# =========================
def classify_candidates(candidates: List[Dict],
                        threshold_strong: float = 75.0,
                        threshold_borderline: float = 55.0) -> Dict:

    strong, borderline, weak = [], [], []

    for c in candidates:
        score = c.get("final_score", 0)

        if score >= threshold_strong:
            strong.append(c)

        elif score >= threshold_borderline:
            borderline.append(c)

        else:
            weak.append(c)

    return {
        "strong": strong,
        "borderline": borderline,
        "weak": weak
    }


# =========================
# 🔹 AGENT DECISION SUMMARY
# =========================
def agent_recommendation(classified: Dict) -> str:
    strong = classified["strong"]
    borderline = classified["borderline"]
    weak = classified["weak"]

    total = len(strong) + len(borderline) + len(weak)

    if total == 0:
        return "No candidates analyzed. Please upload resumes."

    msg = [
        f"Total candidates evaluated: {total}.",
        f"Strong matches: {len(strong)}",
        f"Borderline matches: {len(borderline)}",
        f"Weak matches: {len(weak)}",
    ]

    if len(strong) == 0 and len(borderline) > 0:
        msg.append("No strong matches — consider reviewing borderline candidates manually.")

    elif len(strong) > 0:
        names = [c.get('file_name', 'Candidate') for c in strong][:3]
        msg.append(f"Recommended next step → Shortlist {len(strong)} strong candidates.")
        msg.append(f"Top picks: {', '.join(names)}")

    else:
        msg.append("No suitable profiles. Suggest widening search or updating JD.")

    return " ".join(msg)


# =========================
# 🔹 HR EMAIL DRAFT GENERATOR
# =========================
def make_hr_email_draft(role_title: str,
                        strong_candidates: List[Dict]) -> str:

    if not strong_candidates:
        return (
            "Subject: Resume Screening Update\n\n"
            "Hi,\n\n"
            "Screening completed but no strong candidates matched.\n"
            "Recommend expanding the search pool or adjusting requirements.\n\n"
            "Regards,\nHR Assistant Agent"
        )

    email = [
        f"Subject: Shortlisted Candidates for {role_title}\n",
        "Hello,\n",
        f"I have completed initial screening for the **{role_title}** role.\n",
        "Recommended candidates for interview:\n"
    ]

    for c in strong_candidates:
        name = c.get('file_name',"Candidate")
        score = c.get("final_score", 0)
        exp = c.get("total_experience")
        skills = ", ".join(c.get("skills", [])[:8])
        email.append(f"- {name} | Score {score:.1f} | {exp} yrs | Skills: {skills}")

    email.append("\nPlease review and confirm who should be scheduled.\n")
    email.append("Regards,\nHR Screening Agent")

    return "\n".join(email)
