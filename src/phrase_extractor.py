import re


class PhraseExtractor:

    def extract_phrases(self, text):

        phrases = []

        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # bullet points
            if line.startswith(("-", "•", "*")):

                phrase = re.sub(
                    r"^[-•*]\s*",
                    "",
                    line
                )

                phrase = phrase.strip().lower()

                if len(phrase) > 2:
                    phrases.append(phrase)

        return sorted(list(set(phrases)))