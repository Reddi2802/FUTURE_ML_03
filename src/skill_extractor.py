import pandas as pd


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

        return list(set(esco_skills + custom_skills))