from openai import OpenAI
import json

client = OpenAI()

def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior hiring manager

User goal: "{user_goal}"

Strict Rules:
-Identify real gaps
-Make output DIFFERENT based on goal
-
-

Return only JSON:
{{
"skills:[],
"miss_skills": [],
"roadmap": [],
"in_q":[]
}}

Resume:
{resume_text}

"""
    try:
        responce = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content":"You'er a strict hiring manager."}
                {"role": "user", "content":prompt}
            ]
        )

        content = responce.choices[0].message.content.strip()

        start = content.find("{")
        end = content.rfind("}")+1

        return json.loads(content[start:end])
    

    except Exception as e:
        return {
            "skills":[],
            "miss_skills":[],
            "roadmap":[],
            "in_q":[],
            "error": str(e)
        }
    