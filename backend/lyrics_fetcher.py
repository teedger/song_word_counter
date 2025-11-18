"""
Lyrics Fetcher - Downloads lyrics from Genius API
"""
import time
from typing import List, Dict, Optional
import lyricsgenius
from tqdm import tqdm
import config
from backend.cache_manager import CacheManager


class LyricsFetcher:
    """Fetches lyrics from Genius API with caching support"""

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the lyrics fetcher

        Args:
            api_token: Genius API token (optional, defaults to config)
        """
        self.api_token = api_token or config.GENIUS_API_TOKEN

        if not self.api_token:
            raise ValueError(
                "Genius API token not found. Please set GENIUS_API_TOKEN in .env file. "
                "Get your free token at: https://genius.com/api-clients"
            )

        # Initialize Genius API client
        self.genius = lyricsgenius.Genius(
            self.api_token,
            skip_non_songs=True,
            excluded_terms=["(Remix)", "(Live)", "(Demo)"],
            remove_section_headers=True,
            verbose=False,
            timeout=15
        )

        self.cache_manager = CacheManager()

    def fetch_artist_lyrics(
        self,
        artist_name: str,
        max_songs: Optional[int] = None,
        use_cache: bool = True
    ) -> Dict:
        """
        Fetch all lyrics for an artist

        Args:
            artist_name: Name of the artist
            max_songs: Maximum number of songs to fetch (None for all)
            use_cache: Whether to use cached data if available

        Returns:
            Dictionary containing artist info and lyrics data
        """
        # Check cache first
        if use_cache:
            cached_data = self.cache_manager.get_cached_data(artist_name)
            if cached_data:
                print(f"✓ Loaded {artist_name} from cache")
                return cached_data['data']

        print(f"Fetching lyrics for {artist_name}...")

        try:
            # Search for artist
            artist = self.genius.search_artist(
                artist_name,
                max_songs=max_songs or config.MAX_SONGS_PER_ARTIST,
                sort="popularity"
            )

            if not artist:
                raise ValueError(f"Artist '{artist_name}' not found on Genius")

            # Extract lyrics from songs
            songs_data = []
            print(f"Processing {len(artist.songs)} songs...")

            for song in tqdm(artist.songs, desc="Fetching lyrics"):
                if song.lyrics:
                    songs_data.append({
                        'title': song.title,
                        'lyrics': self._clean_lyrics(song.lyrics),
                        'album': song.album,
                        'year': song.year,
                        'url': song.url
                    })

                # Rate limiting
                time.sleep(config.REQUEST_DELAY)

            result = {
                'artist_name': artist.name,
                'total_songs': len(songs_data),
                'songs': songs_data,
                'artist_url': artist.url,
                'fetched_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Save to cache
            if use_cache:
                self.cache_manager.save_to_cache(artist_name, result)
                print(f"✓ Cached data for {artist_name}")

            return result

        except Exception as e:
            raise Exception(f"Error fetching lyrics for {artist_name}: {str(e)}")

    def _clean_lyrics(self, lyrics: str) -> str:
        """
        Clean up lyrics text

        Args:
            lyrics: Raw lyrics string

        Returns:
            Cleaned lyrics string
        """
        if not lyrics:
            return ""

        # Remove common artifacts
        lyrics = lyrics.replace('\n', ' ')
        lyrics = lyrics.replace('\\n', ' ')

        # Remove Genius footer (usually "XX Embed" or "XX Contributors")
        if 'Embed' in lyrics:
            lyrics = lyrics[:lyrics.rfind('Embed')]
        if 'Contributors' in lyrics:
            lyrics = lyrics[:lyrics.rfind('Contributors')]

        # Remove section markers [Verse], [Chorus], etc.
        import re
        lyrics = re.sub(r'\[.*?\]', '', lyrics)

        # Remove parenthetical annotations
        lyrics = re.sub(r'\(.*?\)', '', lyrics)

        # Clean up whitespace
        lyrics = ' '.join(lyrics.split())

        return lyrics.strip()

    def search_artist(self, query: str) -> List[Dict]:
        """
        Search for artists by name

        Args:
            query: Search query

        Returns:
            List of matching artists with basic info
        """
        try:
            response = self.genius.search_artists(query, per_page=5)
            artists = []

            for hit in response.get('sections', [{}])[0].get('hits', []):
                artist_data = hit.get('result', {})
                artists.append({
                    'name': artist_data.get('name', ''),
                    'url': artist_data.get('url', ''),
                    'image_url': artist_data.get('image_url', ''),
                })

            return artists
        except Exception as e:
            print(f"Error searching for artist: {e}")
            return []

    def get_cached_artists(self) -> List[str]:
        """Get list of cached artists"""
        return self.cache_manager.get_cached_artists()
