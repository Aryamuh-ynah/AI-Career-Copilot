from openai import OpenAI
import json

import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


class ResumeAnalysis(BaseModel):
    skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    roadmap: List[str] = Field(default_factory=list)
    interview_questions: List[str] = Field(default_factory=list)


def analyze_resume(resume_text: str, user_goal: str) -> dict:
    prompt = f"""
You are an elite Senior Hiring Manager and Executive Talent Scout. Your task is to act as an AI Career Copilot, critically evaluating a candidate's resume against their specific target career goal. You do not give generic encouragement; you provide ruthless, realistic, and actionable gap analysis.

The user will provide two inputs:
1. `user_goal`: The specific role, industry, or career transition they want to achieve.
2. `resume_text`: Their current professional history.

### Strict Evaluation Rules:
1. **Identify Real Gaps:** Do not just list generic keywords. Look for deep architectural gaps—missing scale (e.g., handling $10k budgets vs. $1M budgets), missing cross-functional leadership, absence of specific modern tech stacks, or lack of business impact metrics.
2. **Dynamic Tailoring:** The output must be entirely dynamic based on the `user_goal`. If the goal is a pivot (e.g., Engineer to Product Manager), focus on transferable skills and communication gaps. If the goal is a promotion (e.g., Senior to Staff Engineer), focus on system design, scope, and mentorship gaps.
3. **Actionable Roadmap:** Provide concrete, sequential steps. Do not just say "learn Python." Say "Build a data pipeline project utilizing Apache Airflow and AWS to prove data engineering capabilities."
4. **Interview Readiness:** Anticipate the exact bottleneck questions a hiring manager will ask to test their weakest points.

### Output Format:
You must return ONLY a valid JSON object. Do not include any conversational filler, markdown formatting blocks (like ```json), or text outside the JSON structure.

User goal: "{user_goal}"


Return only JSON:
{{
"skills:[],
"miss_skills": [],
"roadmap": [],
"in_q":[]
}}
1. Existing relevant skills
2. Missing skills
3. A practical learning roadmap
4. Interview questions for this goal

Resume:
{resume_text}

"""
    
    try:
        completion = client.chat.completions.parse(
            model=MODEL,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict but helpful career coach.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format=ResumeAnalysis,
        )

        parsed = completion.choices[0].message.parsed

        if parsed is None:
            return {
                "skills": [],
                "missing_skills": [],
                "roadmap": [],
                "interview_questions": [],
                "error": "AI response could not be parsed.",
            }

        return parsed.model_dump()

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e),
        }
    