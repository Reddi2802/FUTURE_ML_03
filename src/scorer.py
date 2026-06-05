class CandidateScorer:

    def skill_overlap_score(
        self,
        candidate_skills,
        required_skills
    ):

        if len(required_skills) == 0:
            return 0

        matched = set(candidate_skills).intersection(
            set(required_skills)
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