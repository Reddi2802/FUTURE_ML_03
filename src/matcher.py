from sentence_transformers import SentenceTransformer, util


class SemanticMatcher:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def similarity_score(
        self,
        resume_text: str,
        job_description: str
    ) -> float:

        resume_embedding = self.model.encode(
            resume_text,
            convert_to_tensor=True
        )

        job_embedding = self.model.encode(
            job_description,
            convert_to_tensor=True
        )

        similarity = util.cos_sim(
            resume_embedding,
            job_embedding
        )

        return float(similarity)