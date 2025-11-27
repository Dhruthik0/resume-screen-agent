Designed for HR teams who want speed and clarity.

This agent reads job descriptions, analyzes resumes, ranks candidates, highlights the best matches, and even drafts an HR-ready shortlist email automatically.
Instead of manually reading every resume, you upload them — the agent thinks, compares, decides, and recommends.

Less time screening. More time interviewing the right people.

 What this Agent Can Do
Feature	- What it actually means
JD understanding:The agent checks if the Job Description is clear or missing details
Resume parsing:Extracts skills, text, experience from PDF/DOCX/TXT
Intelligent scoring:Scores each candidate on semantic relevance, skills & experience
Classification:Categorizes as Strong, Borderline, Weak match
HR email draft:Generates a ready-to-send shortlist email for hiring managers
CSV export:One-click download of ranked/shortlisted candidates

This isn’t a chatbot — it’s an autonomous evaluation system.

Why it feels like a real agent

The agent doesn’t just output numbers.
It thinks, makes judgements, and takes action.

If JD is incomplete → it asks for clarification

If candidates are weak → it recommends next steps

If strong profiles exist → it suggests who to interview

If needed → it drafts an email summarizing them for HR

You don’t instruct it line-by-line.
You give input → it makes decisions on its own.

That’s what makes it an Agent — not just a script.

              ┌───────────────┐
              │  Streamlit UI │
              └───────┬───────┘
                      │ Inputs JD + CVs
                      ▼
            ┌────────────────────┐
            │  Resume Parser     │
            │ (skills, text, exp)│
            └─────────┬──────────┘
                      ▼
       ┌───────────────────────────┐
       │ Embedding Engine (MiniLM) │
       └───────────┬───────────────┘
                   ▼
          ┌─────────────────┐
          │   Ranker        │
          │ semantic + skill│
          │ score + exp     │
          └──────┬─────────-┘
                 ▼
         ┌───────────────────┐
         │ Agent Logic       │
         │ classify + decide │
         │ generate email    │
         └──────┬───────────-┘
                ▼
        ┌─────────────────────┐
        │ HR Shortlist Output │
        └─────────────────────┘

git clone https://github.com/<your-username>/resume-screen-agent
cd resume-screen-agent

python -m venv venv
source venv/bin/activate       
pip install -r requirements.txt

cd app
streamlit run main.py
