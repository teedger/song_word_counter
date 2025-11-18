"""
Configuration settings for the Artist Lyrics Analyzer
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN", "")

# Cache Settings
CACHE_DIR = "data/cache"
PRELOADED_DIR = "data/preloaded"
CACHE_EXPIRY_DAYS = 30

# Analysis Settings
MIN_WORD_LENGTH = 3  # Minimum word length to consider
MAX_SONGS_PER_ARTIST = 100  # Limit for performance

# Stop Words - Common words to exclude
CUSTOM_STOP_WORDS = {
    # Pronouns
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',

    # Articles
    'a', 'an', 'the',

    # Prepositions
    'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any',
    'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between',
    'both', 'but', 'by', 'can', 'cannot', 'could', 'did', 'do', 'does', 'doing',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have',
    'having', 'here', 'how', 'if', 'in', 'into', 'is', 'it', 'just', 'more', 'most',
    'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'out', 'over', 'own', 'same', 'so', 'some', 'such', 'than', 'that', 'the',
    'then', 'there', 'these', 'this', 'those', 'through', 'to', 'too', 'under',
    'until', 'up', 'very', 'was', 'were', 'what', 'when', 'where', 'which', 'while',
    'who', 'why', 'will', 'with', 'would',

    # Common song structure markers
    'chorus', 'verse', 'bridge', 'intro', 'outro', 'hook', 'pre-chorus', 'refrain',

    # Common filler words
    'yeah', 'oh', 'ah', 'uh', 'ooh', 'la', 'na', 'da', 'huh', 'hey', 'yo',
    'mmm', 'hmm', 'whoa', 'woah',
}

# Visualization Settings
COLOR_PALETTE = {
    'background': '#0a0e27',
    'primary': '#ff006e',
    'secondary': '#8338ec',
    'accent': '#06ffa5',
    'text_primary': '#ffffff',
    'text_secondary': '#e0e0e0',
    'gradient_start': '#8338ec',
    'gradient_end': '#ff006e',
}

# Pre-loaded artists (popular artists with pre-computed data)
FEATURED_ARTISTS = [
    'Rihanna',
    'Kanye West',
    'The Weeknd',
    'Travis Scott',
    'Drake',
    'Beyoncé',
    'Taylor Swift',
    'Kendrick Lamar',
]

# App Settings
APP_TITLE = "🎵 Artist Lyrics Analyzer"
APP_DESCRIPTION = """
Discover the unique vocabulary and lyrical diversity of your favorite artists.
Search for any artist to analyze their entire discography!
"""

# Rate limiting (Genius API)
REQUEST_DELAY = 0.5  # Seconds between API requests
MAX_RETRIES = 3
