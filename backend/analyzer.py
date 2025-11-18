"""
Analyzer - Performs statistical analysis on lyrics data
"""
from typing import Dict, List, Tuple
import pandas as pd
from backend.text_processor import TextProcessor


class LyricsAnalyzer:
    """Analyzes lyrics data and generates statistics"""

    def __init__(self):
        """Initialize the analyzer"""
        self.text_processor = TextProcessor()

    def analyze_artist(self, artist_data: Dict) -> Dict:
        """
        Perform comprehensive analysis on artist's lyrics

        Args:
            artist_data: Dictionary containing artist info and songs

        Returns:
            Dictionary with analysis results
        """
        songs = artist_data.get('songs', [])

        if not songs:
            raise ValueError("No songs found in artist data")

        # Extract all lyrics
        all_lyrics = [song['lyrics'] for song in songs if song.get('lyrics')]

        # Process all lyrics
        batch_results = self.text_processor.process_lyrics_batch(all_lyrics)

        # Get top words
        top_words = self._get_top_words(batch_results['word_frequency'], top_n=50)

        # Calculate vocabulary diversity
        diversity_score = self._calculate_diversity_score(
            batch_results['unique_words'],
            batch_results['total_words']
        )

        # Analyze per-song statistics
        song_stats = self._analyze_songs_individually(songs)

        # Prepare results
        analysis = {
            'artist_name': artist_data.get('artist_name', 'Unknown'),
            'total_songs_analyzed': len(all_lyrics),
            'total_words': batch_results['total_words'],
            'unique_words': batch_results['unique_words'],
            'vocabulary_diversity_score': diversity_score,
            'avg_unique_words_per_song': round(batch_results['avg_unique_per_song'], 2),
            'top_words': top_words,
            'word_frequency': batch_results['word_frequency'],
            'all_unique_words_list': sorted(batch_results['all_unique_words']),
            'song_statistics': song_stats,
            'most_verbose_song': self._get_most_verbose_song(song_stats),
            'most_unique_song': self._get_most_unique_song(song_stats),
        }

        return analysis

    def _get_top_words(self, word_frequency: Dict[str, int], top_n: int = 50) -> List[Tuple[str, int]]:
        """
        Get top N most frequent words

        Args:
            word_frequency: Dictionary of word frequencies
            top_n: Number of top words to return

        Returns:
            List of tuples (word, count) sorted by frequency
        """
        sorted_words = sorted(
            word_frequency.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_words[:top_n]

    def _calculate_diversity_score(self, unique_words: int, total_words: int) -> float:
        """
        Calculate vocabulary diversity score (0-10)

        Higher score = more diverse vocabulary
        Score is based on unique words / total words ratio, scaled to 10

        Args:
            unique_words: Number of unique words
            total_words: Total word count

        Returns:
            Diversity score (0-10)
        """
        if total_words == 0:
            return 0.0

        # Calculate ratio
        ratio = unique_words / total_words

        # Scale to 0-10 (typical ratio is 0.1-0.5 for song lyrics)
        # We use a logarithmic scale to better differentiate scores
        score = min(10.0, ratio * 20)  # Scale up

        return round(score, 2)

    def _analyze_songs_individually(self, songs: List[Dict]) -> List[Dict]:
        """
        Analyze each song individually

        Args:
            songs: List of song dictionaries

        Returns:
            List of song statistics
        """
        song_stats = []

        for song in songs:
            lyrics = song.get('lyrics', '')
            if not lyrics:
                continue

            words = self.text_processor.process_text(lyrics)
            unique_words = set(words)
            word_freq = self.text_processor.get_word_frequency(lyrics)

            # Get top 10 words for this song
            top_words = self._get_top_words(word_freq, top_n=10)

            song_stats.append({
                'title': song.get('title', 'Unknown'),
                'total_words': len(words),
                'unique_words': len(unique_words),
                'diversity_ratio': len(unique_words) / len(words) if words else 0,
                'top_words': top_words,
                'year': song.get('year'),
                'album': song.get('album'),
            })

        return song_stats

    def _get_most_verbose_song(self, song_stats: List[Dict]) -> Dict:
        """Get the song with most total words"""
        if not song_stats:
            return {}

        return max(song_stats, key=lambda x: x['total_words'])

    def _get_most_unique_song(self, song_stats: List[Dict]) -> Dict:
        """Get the song with most unique words"""
        if not song_stats:
            return {}

        return max(song_stats, key=lambda x: x['unique_words'])

    def compare_artists(self, analyses: List[Dict]) -> pd.DataFrame:
        """
        Compare multiple artists

        Args:
            analyses: List of analysis dictionaries from analyze_artist()

        Returns:
            DataFrame with comparison data
        """
        comparison_data = []

        for analysis in analyses:
            comparison_data.append({
                'Artist': analysis['artist_name'],
                'Total Songs': analysis['total_songs_analyzed'],
                'Unique Words': analysis['unique_words'],
                'Total Words': analysis['total_words'],
                'Diversity Score': analysis['vocabulary_diversity_score'],
                'Avg Unique/Song': analysis['avg_unique_words_per_song'],
                'Most Used Word': analysis['top_words'][0][0] if analysis['top_words'] else 'N/A',
            })

        return pd.DataFrame(comparison_data)

    def get_word_usage_timeline(self, song_stats: List[Dict]) -> pd.DataFrame:
        """
        Create timeline of vocabulary usage over years

        Args:
            song_stats: List of song statistics with year data

        Returns:
            DataFrame with timeline data
        """
        # Filter songs with year information
        songs_with_year = [s for s in song_stats if s.get('year')]

        if not songs_with_year:
            return pd.DataFrame()

        # Group by year
        timeline_data = {}
        for song in songs_with_year:
            year = song['year']
            if year not in timeline_data:
                timeline_data[year] = {
                    'year': year,
                    'songs': 0,
                    'avg_unique_words': 0,
                    'total_unique': 0
                }

            timeline_data[year]['songs'] += 1
            timeline_data[year]['total_unique'] += song['unique_words']

        # Calculate averages
        for year_data in timeline_data.values():
            year_data['avg_unique_words'] = round(
                year_data['total_unique'] / year_data['songs'], 2
            )

        df = pd.DataFrame(list(timeline_data.values()))
        return df.sort_values('year')
