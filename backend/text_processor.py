"""
Text Processor - Tokenizes and cleans lyrics text
"""
import re
from typing import List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import config


class TextProcessor:
    """Processes lyrics text for analysis"""

    def __init__(self):
        """Initialize text processor and download required NLTK data"""
        self._download_nltk_data()

        # Combine NLTK stopwords with custom stop words
        try:
            nltk_stopwords = set(stopwords.words('english'))
        except:
            nltk_stopwords = set()

        self.stop_words = nltk_stopwords.union(config.CUSTOM_STOP_WORDS)

    def _download_nltk_data(self):
        """Download required NLTK datasets"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        try:
            tokens = word_tokenize(text.lower())
        except:
            # Fallback to simple split if NLTK fails
            tokens = text.lower().split()

        return tokens

    def clean_word(self, word: str) -> str:
        """
        Clean a single word

        Args:
            word: Input word

        Returns:
            Cleaned word
        """
        # Remove punctuation and special characters
        word = re.sub(r'[^\w\s]', '', word)

        # Remove numbers
        word = re.sub(r'\d+', '', word)

        return word.strip()

    def is_valid_word(self, word: str) -> bool:
        """
        Check if word should be included in analysis

        Args:
            word: Word to check

        Returns:
            True if word is valid, False otherwise
        """
        # Check minimum length
        if len(word) < config.MIN_WORD_LENGTH:
            return False

        # Check if it's a stop word
        if word.lower() in self.stop_words:
            return False

        # Check if it's all letters
        if not word.isalpha():
            return False

        return True

    def process_text(self, text: str) -> List[str]:
        """
        Process text and return list of valid words

        Args:
            text: Input text

        Returns:
            List of processed, valid words
        """
        # Tokenize
        tokens = self.tokenize(text)

        # Clean and filter
        processed_words = []
        for token in tokens:
            cleaned = self.clean_word(token)
            if cleaned and self.is_valid_word(cleaned):
                processed_words.append(cleaned)

        return processed_words

    def get_unique_words(self, text: str) -> Set[str]:
        """
        Get set of unique words from text

        Args:
            text: Input text

        Returns:
            Set of unique words
        """
        words = self.process_text(text)
        return set(words)

    def get_word_frequency(self, text: str) -> dict:
        """
        Get word frequency count

        Args:
            text: Input text

        Returns:
            Dictionary mapping words to their counts
        """
        words = self.process_text(text)
        frequency = {}

        for word in words:
            frequency[word] = frequency.get(word, 0) + 1

        return frequency

    def process_lyrics_batch(self, lyrics_list: List[str]) -> dict:
        """
        Process multiple lyrics texts and combine results

        Args:
            lyrics_list: List of lyrics texts

        Returns:
            Dictionary with combined statistics
        """
        all_words = []
        all_unique_words = set()
        song_word_counts = []

        for lyrics in lyrics_list:
            words = self.process_text(lyrics)
            unique_words = set(words)

            all_words.extend(words)
            all_unique_words.update(unique_words)
            song_word_counts.append(len(unique_words))

        # Calculate frequency across all songs
        word_frequency = {}
        for word in all_words:
            word_frequency[word] = word_frequency.get(word, 0) + 1

        return {
            'total_words': len(all_words),
            'unique_words': len(all_unique_words),
            'all_unique_words': all_unique_words,
            'word_frequency': word_frequency,
            'avg_unique_per_song': sum(song_word_counts) / len(song_word_counts) if song_word_counts else 0,
            'song_word_counts': song_word_counts
        }
