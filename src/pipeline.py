from src.pdf_parser import PDFParser
from src.ranker import ResumeRanker


class ResumePipeline:

    def __init__(self, esco_path):
        self.parser = PDFParser()
        self.ranker = ResumeRanker(esco_path)

    def rank_pdf_resume(self, pdf_path, job_description):
        resume_text = self.parser.extract_text(pdf_path)
        results = self.ranker.rank_candidates([resume_text], job_description)
        return results[0]