#!/usr/bin/env python3
"""
Pre-load and cache featured artists for faster initial experience
"""
import sys
from backend.lyrics_fetcher import LyricsFetcher
from backend.analyzer import LyricsAnalyzer
import config
import json
from pathlib import Path


def preload_artist(fetcher, analyzer, artist_name, max_songs=50):
    """
    Preload and analyze an artist

    Args:
        fetcher: LyricsFetcher instance
        analyzer: LyricsAnalyzer instance
        artist_name: Name of artist to preload
        max_songs: Maximum songs to fetch
    """
    print(f"\n{'='*60}")
    print(f"Processing: {artist_name}")
    print('='*60)

    try:
        # Fetch lyrics
        print(f"📥 Fetching lyrics for {artist_name}...")
        artist_data = fetcher.fetch_artist_lyrics(artist_name, max_songs=max_songs)

        # Analyze
        print(f"🔍 Analyzing {artist_data['total_songs']} songs...")
        analysis = analyzer.analyze_artist(artist_data)

        # Save preloaded data
        preload_path = Path(config.PRELOADED_DIR) / f"{artist_name.replace(' ', '_').lower()}_analysis.json"
        with open(preload_path, 'w', encoding='utf-8') as f:
            # Save a summary (not full lyrics to save space)
            summary = {
                'artist_name': analysis['artist_name'],
                'total_songs_analyzed': analysis['total_songs_analyzed'],
                'unique_words': analysis['unique_words'],
                'vocabulary_diversity_score': analysis['vocabulary_diversity_score'],
                'top_words': analysis['top_words'][:20],
                'avg_unique_words_per_song': analysis['avg_unique_words_per_song'],
            }
            json.dump(summary, f, indent=2)

        print(f"✅ {artist_name} - Complete!")
        print(f"   📊 Unique Words: {analysis['unique_words']:,}")
        print(f"   🎯 Diversity Score: {analysis['vocabulary_diversity_score']}/10")
        print(f"   🎵 Songs Analyzed: {analysis['total_songs_analyzed']}")

    except Exception as e:
        print(f"❌ Error processing {artist_name}: {str(e)}")


def main():
    """Main preloading function"""
    print("🎵 Artist Lyrics Analyzer - Data Preloader")
    print("=" * 60)

    try:
        # Initialize
        fetcher = LyricsFetcher()
        analyzer = LyricsAnalyzer()

        print(f"\n📋 Preloading {len(config.FEATURED_ARTISTS)} featured artists...")

        # Process each featured artist
        for artist in config.FEATURED_ARTISTS:
            preload_artist(fetcher, analyzer, artist, max_songs=50)

        print("\n" + "=" * 60)
        print("✅ Preloading complete!")
        print("=" * 60)
        print("\n💡 Tip: Preloaded data is cached and ready for instant access in the app")

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔑 Make sure you have set up your Genius API token in the .env file")
        print("   Get your free token at: https://genius.com/api-clients")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Preloading interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
