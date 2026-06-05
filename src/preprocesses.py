import re
import string


class TextPreprocessor:

    def __init__(self):
        self.stopwords = {
            "a", "an", "the", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "by", "from", "is", "was",
            "are", "were", "be", "been", "has", "have", "had",
            "do", "does", "did", "will", "would", "could",
            "should", "may", "might"
        }

    def clean_for_embeddings(self, text: str) -> str:
        """
        Minimal cleaning.
        Preserve natural language structure for Sentence Transformers.
        """

        if not isinstance(text, str):
            return ""

        text = text.lower()

        # remove urls
        text = re.sub(r"http\S+|www\S+", " ", text)

        # normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def clean_for_skills(self, text: str) -> str:
        """
        More aggressive cleaning.
        Optimized for skill extraction.
        """

        if not isinstance(text, str):
            return ""

        text = text.lower()

        # remove urls
        text = re.sub(r"http\S+|www\S+", " ", text)

        # preserve technical tokens
        text = text.replace("c++", "cplusplus")
        text = text.replace("c#", "csharp")
        text = text.replace(".net", "dotnet")
        text = text.replace("node.js", "nodejs")
        text = text.replace("scikit-learn", "scikitlearn")

        # remove punctuation
        text = re.sub(
            rf"[{re.escape(string.punctuation)}]",
            " ",
            text
        )

        # normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # remove stopwords
        tokens = text.split()

        tokens = [
            token
            for token in tokens
            if token not in self.stopwords
        ]

        return " ".join(tokens)

    def clean_resume(self, text: str) -> str:
        """
        Resume-specific cleanup.
        """

        text = self.clean_for_embeddings(text)

        noise_patterns = [
            r"company name",
            r"city\s*,?\s*state",
            r"references available upon request"
        ]

        for pattern in noise_patterns:
            text = re.sub(pattern, " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()