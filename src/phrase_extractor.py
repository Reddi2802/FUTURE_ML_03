import re


class PhraseExtractor:

    def extract_phrases(self, text):

        phrases = set()

        lines = text.split("\n")

        inside_requirements = False

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if "requirements" in line.lower():
                inside_requirements = True
                continue

            if not inside_requirements:
                continue

            if line.startswith(("-", "•", "*")):

                phrase = re.sub(
                    r"^[-•*]\s*",
                    "",
                    line
                )

                phrase = phrase.strip().lower()

                if len(phrase) > 2:
                    phrases.add(phrase)

        return sorted(list(phrases))