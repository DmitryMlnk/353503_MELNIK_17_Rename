# Text analysis module for Lab 3 - Task 2
# Developer: Dmitry Melnik
# Date: May 01, 2025

import re

class TextProcessor:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        """Get the text content."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the text content."""
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        self._text = value

    def __str__(self):
        """String representation of the text processor."""
        return f"TextProcessor with content of length {len(self._text)}"

class TextAnalyzer(TextProcessor):
    _analysis_count = 0  # Static attribute

    def __init__(self, text):
        super().__init__(text)
        self._results = {}  # Dynamic attribute
        TextAnalyzer._analysis_count += 1

    @property
    def results(self):
        """Get the analysis results."""
        return self._results

    def count_sentences(self):
        """Count total sentences and classify by type."""
        sentences = re.split(r'[.!?]+', self.text)
        total = len([s for s in sentences if s.strip()])
        declarative = len(re.findall(r'[^\.!?]*\.[^\.!?]*', self.text))
        interrogative = len(re.findall(r'[^\?]*\?[^\?]*', self.text))
        imperative = len(re.findall(r'[^\!]*\![^\!]*', self.text))
        return total, declarative, interrogative, imperative

    def avg_sentence_length(self):
        """Calculate average sentence length (words only)."""
        sentences = re.split(r'[.!?]+', self.text)
        words = [len(re.findall(r'\w+', s)) for s in sentences if s.strip()]
        return sum(words) / len(words) if words else 0

    def avg_word_length(self):
        """Calculate average word length in characters."""
        words = re.findall(r'\w+', self.text)
        return sum(len(word) for word in words) / len(words) if words else 0

    def count_smileys(self):
        """Count valid smileys in the text."""
        pattern = r'[:;]-*[\(\)\[\]]+'
        return len(re.findall(pattern, self.text))

    def find_f_to_y_words(self):
        """Find words containing letters from 'f' to 'y'."""
        words = re.findall(r'\w+', self.text)
        return [w for w in words if any(c in w.lower() for c in 'fghijklmnopqrstuvwxyz')]

    def extract_prices(self):
        """Extract prices in USD, RUR, EU."""
        pattern = r'\d+\.\d{2}\s?(USD|RUR|EU)\b'
        return re.findall(pattern, self.text)

    def short_words(self, max_length=7):
        """Count words shorter than max_length."""
        return len(re.findall(r'\b\w{1,' + str(max_length-1) + r'}\b', self.text))

    def shortest_word_ending_a(self):
        """Find the shortest word ending with 'a'."""
        words = [w for w in re.findall(r'\w+', self.text) if w.endswith('a')]
        return min(words, key=len) if words else None

    def words_by_length_desc(self):
        """Sort words by length in descending order."""
        words = re.findall(r'\w+', self.text)
        return sorted(words, key=len, reverse=True)

    def __lt__(self, other):
        """Polymorphism: Compare TextAnalyzers by text length."""
        if not isinstance(other, TextAnalyzer):
            return NotImplemented
        return len(self._text) < len(other._text)

    def __repr__(self):
        """Detailed string representation."""
        return f"TextAnalyzer(text_length={len(self._text)}, results={self._results})"

    @classmethod
    def get_analysis_count(cls):
        """Class method to get total analysis count."""
        return cls._analysis_count