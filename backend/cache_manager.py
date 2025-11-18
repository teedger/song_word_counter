"""
Cache Manager for storing and retrieving artist lyrics data
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List
import config


class CacheManager:
    """Manages caching of lyrics data to minimize API calls"""

    def __init__(self, cache_dir: str = config.CACHE_DIR):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, artist_name: str) -> Path:
        """Generate cache file path for an artist"""
        safe_name = "".join(c for c in artist_name if c.isalnum() or c in (' ', '-', '_'))
        safe_name = safe_name.replace(' ', '_').lower()
        return self.cache_dir / f"{safe_name}.json"

    def is_cached(self, artist_name: str) -> bool:
        """Check if artist data is cached and not expired"""
        cache_path = self._get_cache_path(artist_name)

        if not cache_path.exists():
            return False

        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cached_date = datetime.fromisoformat(data.get('cached_at', ''))
                expiry_date = cached_date + timedelta(days=config.CACHE_EXPIRY_DAYS)
                return datetime.now() < expiry_date
        except (json.JSONDecodeError, KeyError, ValueError):
            return False

    def get_cached_data(self, artist_name: str) -> Optional[Dict]:
        """Retrieve cached data for an artist"""
        if not self.is_cached(artist_name):
            return None

        cache_path = self._get_cache_path(artist_name)
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    def save_to_cache(self, artist_name: str, data: Dict) -> bool:
        """Save artist data to cache"""
        cache_path = self._get_cache_path(artist_name)

        cache_data = {
            'artist_name': artist_name,
            'cached_at': datetime.now().isoformat(),
            'data': data
        }

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving to cache: {e}")
            return False

    def clear_cache(self, artist_name: Optional[str] = None) -> None:
        """Clear cache for specific artist or all artists"""
        if artist_name:
            cache_path = self._get_cache_path(artist_name)
            if cache_path.exists():
                cache_path.unlink()
        else:
            # Clear all cache files
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()

    def get_cached_artists(self) -> List[str]:
        """Get list of all cached artists"""
        cached_artists = []
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cached_artists.append(data.get('artist_name', ''))
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        return cached_artists
