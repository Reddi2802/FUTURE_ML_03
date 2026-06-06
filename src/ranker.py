from src.skill_extractor import SkillExtractor
from src.matcher import SemanticMatcher
from src.scorer import CandidateScorer
from src.phrase_extractor import PhraseExtractor


class ResumeRanker:

    def __init__(self, esco_path):

        self.extractor = SkillExtractor(esco_path)
        self.matcher = SemanticMatcher()
        self.scorer = CandidateScorer()
        self.phrase_extractor = PhraseExtractor()

    def rank_candidates(
        self,
        resumes,
        job_description
    ):

        # -------------------------
        # Extract JD skills
        # -------------------------

        required_skills = set(
            self.extractor.extract_skills(
                job_description
            )
        )

        required_skills.update(
            self.phrase_extractor.extract_phrases(
                job_description
            )
        )

        required_skills = list(required_skills)

        results = []

        # -------------------------
        # Score resumes
        # -------------------------

        for idx, resume in enumerate(resumes):

            candidate_skills = self.extractor.extract_skills(
                resume
            )

            semantic_score = (
                self.matcher.similarity_score(
                    resume,
                    job_description
                )
            )

            skill_score = (
                self.scorer.skill_overlap_score(
                    candidate_skills,
                    required_skills
                )
            )

            final_score = (
                self.scorer.final_score(
                    semantic_score,
                    skill_score
                )
            )
            
            print("\nREQUIRED:", required_skills)
            print("CANDIDATE:", candidate_skills)

            print(
                "INTERSECTION:",
                set(candidate_skills).intersection(
                    set(required_skills)
                )
            )

            matched_skills = list(
                set(candidate_skills).intersection(
                    set(required_skills)
                )
            )

            missing_skills = list(
                set(required_skills)
                -
                set(candidate_skills)
            )

            results.append({
                "candidate_id": idx + 1,
                "semantic_score": round(
                    semantic_score,
                    3
                ),
                "skill_score": round(
                    skill_score,
                    3
                ),
                "final_score": round(
                    final_score,
                    3
                ),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills
            })

        results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return results