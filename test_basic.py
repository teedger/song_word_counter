#!/usr/bin/env python3
"""
Basic test script to verify the application components
"""
import sys


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")

    try:
        import config
        print("✓ config")

        from backend.cache_manager import CacheManager
        print("✓ backend.cache_manager")

        from backend.text_processor import TextProcessor
        print("✓ backend.text_processor")

        from backend.analyzer import LyricsAnalyzer
        print("✓ backend.analyzer")

        from backend.lyrics_fetcher import LyricsFetcher
        print("✓ backend.lyrics_fetcher (note: requires API token to initialize)")

        from frontend.visualizations import MusicVisualizer
        print("✓ frontend.visualizations")

        print("\n✅ All modules imported successfully!")
        return True

    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
        return False


def test_text_processor():
    """Test the text processor"""
    print("\n" + "="*60)
    print("Testing TextProcessor...")
    print("="*60)

    from backend.text_processor import TextProcessor

    processor = TextProcessor()

    # Test text
    test_text = """
    I love this song, yeah, yeah!
    The music is so beautiful and the lyrics are amazing.
    [Chorus]
    Oh, baby, don't you know?
    """

    # Process text
    words = processor.process_text(test_text)
    print(f"\n Original text: {test_text[:100]}...")
    print(f"\n Processed words: {words[:10]}...")
    print(f" Total valid words: {len(words)}")

    unique = processor.get_unique_words(test_text)
    print(f" Unique words: {len(unique)}")
    print(f" Sample unique words: {list(unique)[:10]}")

    frequency = processor.get_word_frequency(test_text)
    print(f"\n Top 5 words by frequency:")
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    for word, count in sorted_freq:
        print(f"   {word}: {count}")

    print("\n✅ TextProcessor working correctly!")


def test_cache_manager():
    """Test the cache manager"""
    print("\n" + "="*60)
    print("Testing CacheManager...")
    print("="*60)

    from backend.cache_manager import CacheManager

    cache = CacheManager()

    # Test data
    test_data = {
        'artist_name': 'Test Artist',
        'total_songs': 5,
        'unique_words': 100
    }

    # Save to cache
    cache.save_to_cache('Test Artist', test_data)
    print("\n✓ Data saved to cache")

    # Check if cached
    is_cached = cache.is_cached('Test Artist')
    print(f"✓ Is cached: {is_cached}")

    # Retrieve from cache
    retrieved = cache.get_cached_data('Test Artist')
    print(f"✓ Retrieved data: {retrieved is not None}")

    # Clear test cache
    cache.clear_cache('Test Artist')
    print("✓ Cache cleared")

    print("\n✅ CacheManager working correctly!")


def test_visualizer():
    """Test the visualizer"""
    print("\n" + "="*60)
    print("Testing MusicVisualizer...")
    print("="*60)

    from frontend.visualizations import MusicVisualizer

    visualizer = MusicVisualizer()

    # Test data
    word_freq = {
        'love': 50,
        'heart': 30,
        'soul': 25,
        'music': 20,
        'dance': 15,
    }

    # Test creating a chart
    fig = visualizer.create_top_words_chart(list(word_freq.items()))
    print(f"\n✓ Created top words chart: {type(fig)}")

    # Test gauge
    gauge = visualizer.create_diversity_gauge(7.5)
    print(f"✓ Created diversity gauge: {type(gauge)}")

    # Test word cloud
    wc_img = visualizer.create_word_cloud(word_freq)
    print(f"✓ Created word cloud: {len(wc_img)} bytes")

    print("\n✅ MusicVisualizer working correctly!")


def main():
    """Run all tests"""
    print("\n🧪 Artist Lyrics Analyzer - Component Tests")
    print("="*60)

    # Test imports
    if not test_imports():
        sys.exit(1)

    # Test individual components
    try:
        test_cache_manager()
        test_text_processor()
        test_visualizer()

        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        print("\n💡 Next steps:")
        print("   1. Set up your .env file with Genius API token")
        print("   2. Run: python run.py")
        print("   3. Enjoy analyzing your favorite artists!")

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
