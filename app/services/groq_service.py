import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 SINGLE RESUME ANALYSIS
def analyze_with_groq(resume_text, role, skills, seniority):
    prompt = f"""
You are a TOP 1% AI Hiring Manager.

TASK:
Evaluate this candidate strictly for a competitive hiring process.

RESUME:
{resume_text}

JOB:
Role: {role}
Skills: {skills}
Level: {seniority}

RULES:
- Be strict in scoring
- Not all candidates should get high scores
- Only top candidates should score above 80
- Avoid keyword matching, focus on real depth

OUTPUT JSON:

{{
  "candidate_meta": {{
    "name": "",
    "current_title": ""
  }},
  "scores": {{
    "match_score": 0
  }},
  "skills_analysis": {{
    "strong_skills": []
  }},
  "decision": {{
    "hire_recommendation": "STRONG_HIRE / HIRE / BORDERLINE / REJECT",
    "why_this_candidate": "",
    "top_strengths": [],
    "red_flags": []
  }}
}}
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    response_content = chat.choices[0].message.content

    try:
        cleaned = re.sub(r"```json|```", "", response_content).strip()
        data = json.loads(cleaned)

        return {
            "name": data.get("candidate_meta", {}).get("name", "Unknown"),
            "title": data.get("candidate_meta", {}).get("current_title", ""),
            
            # ✅ FIX: frontend compatible
            "match": int(data.get("scores", {}).get("match_score", 0)),
            
            "skills": data.get("skills_analysis", {}).get("strong_skills", []),

            "summary": data.get("decision", {}).get("why_this_candidate", ""),

            "strengths": data.get("decision", {}).get("top_strengths", []),
            "red_flags": data.get("decision", {}).get("red_flags", []),

            "decision": data.get("decision", {}).get("hire_recommendation", "REJECT")
        }

    except Exception as e:
        print("JSON ERROR:", e)
        return {
            "name": "Unknown",
            "title": "",
            "match": 0,
            "skills": [],
            "summary": "Parsing failed",
            "strengths": [],
            "red_flags": [],
            "decision": "REJECT"
        }


# 🔥 MULTIPLE RESUMES + TOP N FILTER
def analyze_multiple_resumes(resume_texts, role, skills, seniority, top_n=5):
    
    results = []

    for text in resume_texts:
        result = analyze_with_groq(text, role, skills, seniority)
        results.append(result)

    # ✅ SORT BY MATCH SCORE
    results = sorted(results, key=lambda x: x["match"], reverse=True)

    # ✅ TAKE ONLY TOP N
    top_n = int(top_n)
    results = results[:top_n]

    return {
        "results": results,
        "total_candidates": len(resume_texts),
        "selected": len(results),
        "rejected": len(resume_texts) - len(results)
    }