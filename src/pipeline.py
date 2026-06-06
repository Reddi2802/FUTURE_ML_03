from src.pdf_parser import PDFParser
from src.ranker import ResumeRanker
from src.summarizer import Summarizer


class ResumePipeline:

    def __init__(self, esco_path):
        self.parser = PDFParser()
        self.ranker = ResumeRanker(esco_path)
        self.summarizer = Summarizer()

    def rank_pdf_resume(self, pdf_path, job_description):
        resume_text = self.parser.extract_text(pdf_path)
        results = self.ranker.rank_candidates([resume_text], job_description)
        result = results[0]
        result["summary"] = self.summarizer.generate_summary(result)
        return result

    def rank_multiple_resumes(self, pdf_paths, job_description):
        results = []

        for idx, pdf_path in enumerate(pdf_paths):
            resume_text = self.parser.extract_text(pdf_path)
            result = self.ranker.rank_candidates([resume_text], job_description)[0]
            result["candidate_id"] = idx + 1
            result["filename"] = pdf_path.split("\\")[-1].split("/")[-1]
            result["summary"] = self.summarizer.generate_summary(result)
            results.append(result)

        results.sort(key=lambda x: x["final_score"], reverse=True)

        return results