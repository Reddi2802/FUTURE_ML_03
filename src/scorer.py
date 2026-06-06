class CandidateScorer:

    def skill_overlap_score(
        self,
        candidate_skills,
        required_skills
    ):

        candidate_skills = set(candidate_skills)
        required_skills = set(required_skills)

        if len(required_skills) == 0:
            return 0.0

        matched = candidate_skills.intersection(
            required_skills
        )

        return len(matched) / len(required_skills)

    def final_score(
        self,
        semantic_similarity,
        skill_overlap
    ):

        return (
            0.7 * semantic_similarity
            +
            0.3 * skill_overlap
        )