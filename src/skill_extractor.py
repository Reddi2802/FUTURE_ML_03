import pandas as pd
import re


class SkillExtractor:
    def __init__(self, esco_path):
        self.skills = self._load_skills(esco_path)

    def _load_skills(self, esco_path):
        skills_df = pd.read_csv(esco_path)

        esco_skills = (
            skills_df["preferredLabel"]
            .dropna()
            .str.lower()
            .unique()
            .tolist()
        )
        
        alt_skills = (
            skills_df["altLabels"]
            .dropna()
            .str.lower()
            .str.split('\n')
            .explode()
            .str.strip()
            .unique()
            .tolist()
        )

        custom_skills = [
            "python",
            "sql",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "nlp",
            "data science",
            "data analysis",
            "artificial intelligence",
            "aws",
            "azure",
            "gcp",
            "docker",
            "kubernetes",
            "java",
            "javascript",
            "react",
            "node.js",
            "pandas",
            "numpy",
            "scikit-learn",
            "langchain",
            "llm",
            "rag"
        ]

        return list(set(esco_skills + alt_skills + custom_skills))

    def extract_skills(self, text):

        text = text.lower()

        found_skills = set()

        for skill in self.skills:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                found_skills.add(skill)

        found_skills = sorted(
            found_skills,
            key=len,
            reverse=True
        )

        filtered_skills = []

        for skill in found_skills:

            is_subskill = False

            for kept_skill in filtered_skills:

                pattern = r"\b" + re.escape(skill) + r"\b"

                if re.search(
                    pattern,
                    kept_skill
                ):
                    is_subskill = True
                    break

            if not is_subskill:
                filtered_skills.append(skill)

        return sorted(filtered_skills)