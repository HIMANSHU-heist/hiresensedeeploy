from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from services.parser import extract_text_from_pdf
from services.groq_service import analyze_with_groq

router = APIRouter()

@router.post("/analyze")
async def analyze_resumes(
    resumes: List[UploadFile] = File(...),  # ✅ FIXED NAME
    role: str = Form(...),
    skills: str = Form(...),
    seniority: str = Form(...)
):
    results = []

    for file in resumes:
        content = await file.read()
        text = extract_text_from_pdf(content)

        ai_result = analyze_with_groq(text, role, skills, seniority)

        if ai_result:
            results.append(ai_result)

    return {"results": results}