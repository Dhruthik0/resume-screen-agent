import numpy as np

def cosine_sim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def skill_match_score(req_skills, cand_skills):
    req_skills = [s.strip().lower() for s in req_skills if s.strip()]
    cand_skills = [c.lower() for c in cand_skills]
    if not req_skills:
        return 0
    match = len([s for s in req_skills if s in cand_skills])
    return match / len(req_skills)

def experience_score(req_years, cand_years):
    if not req_years or not cand_years:
        return 0.5
    return min(cand_years / req_years, 1.0)

def combine_scores(semantic, skill, experience, w_sem, w_skill, w_exp):
    return semantic*w_sem + skill*w_skill + experience*w_exp

def score_candidates(cands, jd_text, jd_emb, req_skills, req_years, weights):
    for c in cands:
        emb = get_embedding_wrapper(c["text"])
        semantic = cosine_sim(emb, jd_emb)
        skill = skill_match_score(req_skills, c["skills"])
        exp = experience_score(req_years, c["total_experience"])
        final = combine_scores(semantic, skill, exp,
                               weights["w_sem"], weights["w_skill"], weights["w_exp"])
        c["semantic"] = semantic
        c["skill_score"] = skill
        c["experience_score"] = exp
        c["final_score"] = final
    return cands


from embedder import get_embedding as get_embedding_wrapper
