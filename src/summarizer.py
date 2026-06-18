import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class Summarizer:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate_summary(self, result: dict) -> str:

        score = result["final_score"]
        semantic = result["semantic_score"]
        skill_score = result["skill_score"]
        matched = result["matched_skills"]
        missing = result["missing_skills"]

        prompt = f"""
You are an expert technical recruiter. Based on the following candidate analysis, write a short 3-4 sentence professional summary.

Scores:
- Final Score: {score:.0%}
- Semantic Similarity: {semantic:.0%}
- Skill Match: {skill_score:.0%}

Matched Skills: {", ".join(matched) if matched else "None"}
Missing Skills: {", ".join(missing) if missing else "None"}

Write the summary in third person. Be direct and professional. End with a clear recommendation: either shortlist, consider, or reject.
Do not use bullet points. Plain paragraph only.
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Summary unavailable: {str(e)}"