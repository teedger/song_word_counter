"""
Main Streamlit Application for Artist Lyrics Analyzer
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from backend.lyrics_fetcher import LyricsFetcher
from backend.analyzer import LyricsAnalyzer
from frontend.visualizations import MusicVisualizer


# Page config
st.set_page_config(
    page_title="Artist Lyrics Analyzer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for music-inspired theme
def load_custom_css():
    """Load custom CSS styling"""
    st.markdown(f"""
    <style>
        /* Main theme */
        .stApp {{
            background: linear-gradient(135deg, {config.COLOR_PALETTE['background']} 0%, #1a1a2e 100%);
        }}

        /* Headers */
        h1, h2, h3 {{
            color: {config.COLOR_PALETTE['text_primary']} !important;
            font-weight: bold;
        }}

        /* Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, {config.COLOR_PALETTE['primary']}, {config.COLOR_PALETTE['secondary']});
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 30px;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }}

        .stButton>button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(255, 0, 110, 0.4);
        }}

        /* Input boxes */
        .stTextInput>div>div>input {{
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border: 2px solid {config.COLOR_PALETTE['secondary']};
            border-radius: 10px;
        }}

        /* Sidebar */
        .css-1d391kg {{
            background-color: #0f1419;
        }}

        /* Cards */
        .stat-card {{
            background: linear-gradient(135deg, {config.COLOR_PALETTE['primary']}, {config.COLOR_PALETTE['secondary']});
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 10px 0;
        }}

        /* Featured artists */
        .featured-artist {{
            display: inline-block;
            background: rgba(131, 56, 236, 0.3);
            border: 2px solid {config.COLOR_PALETTE['secondary']};
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .featured-artist:hover {{
            background: {config.COLOR_PALETTE['secondary']};
            transform: scale(1.05);
        }}
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'current_artist' not in st.session_state:
        st.session_state.current_artist = None
    if 'fetcher' not in st.session_state:
        try:
            st.session_state.fetcher = LyricsFetcher()
        except ValueError as e:
            st.session_state.fetcher = None
            st.session_state.api_error = str(e)
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = LyricsAnalyzer()
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = MusicVisualizer()


def analyze_artist(artist_name: str, max_songs: int = None):
    """
    Analyze an artist and store results in session state

    Args:
        artist_name: Name of the artist
        max_songs: Maximum number of songs to analyze
    """
    try:
        with st.spinner(f'🎵 Fetching lyrics for {artist_name}...'):
            # Fetch lyrics
            artist_data = st.session_state.fetcher.fetch_artist_lyrics(
                artist_name,
                max_songs=max_songs
            )

        with st.spinner(f'🔍 Analyzing {artist_data["total_songs"]} songs...'):
            # Analyze
            analysis = st.session_state.analyzer.analyze_artist(artist_data)

        st.session_state.analysis_result = analysis
        st.session_state.current_artist = artist_name
        st.success(f'✅ Analysis complete for {analysis["artist_name"]}!')

    except Exception as e:
        st.error(f'❌ Error: {str(e)}')
        st.session_state.analysis_result = None


def render_header():
    """Render the app header"""
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="font-size: 3em; margin-bottom: 10px;">
            {config.APP_TITLE}
        </h1>
        <p style="color: {config.COLOR_PALETTE['text_secondary']}; font-size: 1.2em;">
            {config.APP_DESCRIPTION}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_search_section():
    """Render the search section"""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        artist_query = st.text_input(
            "Search for an artist",
            placeholder="e.g., Rihanna, Kanye West, The Weeknd...",
            label_visibility="collapsed"
        )

    with col2:
        max_songs = st.number_input(
            "Max Songs",
            min_value=10,
            max_value=200,
            value=50,
            step=10
        )

    with col3:
        analyze_button = st.button("🔍 Analyze", use_container_width=True)

    if analyze_button and artist_query:
        analyze_artist(artist_query, max_songs)

    return artist_query


def render_featured_artists():
    """Render featured artists section"""
    st.markdown("### 🎤 Featured Artists")

    # Create columns for featured artists
    cols = st.columns(4)

    for idx, artist in enumerate(config.FEATURED_ARTISTS):
        col_idx = idx % 4
        with cols[col_idx]:
            if st.button(artist, use_container_width=True, key=f"featured_{artist}"):
                analyze_artist(artist, max_songs=50)


def render_analysis_results():
    """Render analysis results"""
    if st.session_state.analysis_result is None:
        st.info("👆 Search for an artist or select a featured artist to begin analysis")
        return

    analysis = st.session_state.analysis_result
    visualizer = st.session_state.visualizer

    # Artist name header
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <h2 style="font-size: 2.5em; color: {config.COLOR_PALETTE['primary']};">
            {analysis['artist_name']}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Statistics cards
    st.markdown(visualizer.create_stats_cards_html(analysis), unsafe_allow_html=True)

    # Diversity gauge
    st.plotly_chart(
        visualizer.create_diversity_gauge(analysis['vocabulary_diversity_score']),
        use_container_width=True
    )

    # Two column layout for visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Top Words")
        st.plotly_chart(
            visualizer.create_top_words_chart(analysis['top_words'], top_n=20),
            use_container_width=True
        )

    with col2:
        st.markdown("### ☁️ Word Cloud")
        word_cloud_img = visualizer.create_word_cloud(analysis['word_frequency'])
        st.markdown(
            f'<img src="data:image/png;base64,{word_cloud_img}" style="width:100%; border-radius: 10px;">',
            unsafe_allow_html=True
        )

    # Timeline chart (if data available)
    if analysis.get('song_statistics'):
        timeline_df = st.session_state.analyzer.get_word_usage_timeline(
            analysis['song_statistics']
        )
        if not timeline_df.empty:
            st.markdown("### 📈 Vocabulary Evolution")
            st.plotly_chart(
                visualizer.create_timeline_chart(timeline_df),
                use_container_width=True
            )

    # Detailed statistics (expandable)
    with st.expander("📋 Detailed Statistics"):
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Total Words (processed)", f"{analysis['total_words']:,}")
            st.metric("Unique Words", f"{analysis['unique_words']:,}")
            st.metric("Songs Analyzed", analysis['total_songs_analyzed'])

        with col2:
            st.metric("Diversity Score", f"{analysis['vocabulary_diversity_score']}/10")
            st.metric("Avg Unique Words/Song", f"{analysis['avg_unique_words_per_song']:.1f}")

            if analysis.get('most_verbose_song'):
                st.metric(
                    "Most Verbose Song",
                    analysis['most_verbose_song']['title']
                )

    # Top 50 words table
    with st.expander("🔝 Top 50 Words Breakdown"):
        import pandas as pd
        top_50_df = pd.DataFrame(
            analysis['top_words'][:50],
            columns=['Word', 'Frequency']
        )
        st.dataframe(top_50_df, use_container_width=True, height=400)


def render_sidebar():
    """Render sidebar with additional options"""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        st.markdown("### 📊 Cache")
        if st.button("Clear Cache"):
            if st.session_state.fetcher:
                st.session_state.fetcher.cache_manager.clear_cache()
                st.success("Cache cleared!")

        st.markdown("### ℹ️ About")
        st.markdown("""
        This app analyzes the lyrical vocabulary of artists by:
        - Fetching lyrics from Genius API
        - Processing and filtering words
        - Calculating unique vocabulary statistics
        - Creating beautiful visualizations

        **Tech Stack:**
        - Python, Streamlit
        - Plotly, WordCloud
        - NLTK, Pandas
        """)

        st.markdown("### 🔑 API Status")
        if st.session_state.fetcher:
            st.success("✅ Genius API Connected")
        else:
            st.error("❌ API Token Missing")
            if hasattr(st.session_state, 'api_error'):
                st.warning(st.session_state.api_error)
                st.markdown("""
                **Setup Instructions:**
                1. Get a free API token at [genius.com/api-clients](https://genius.com/api-clients)
                2. Create a `.env` file in the project root
                3. Add: `GENIUS_API_TOKEN=your_token_here`
                4. Restart the app
                """)


def main():
    """Main application function"""
    load_custom_css()
    initialize_session_state()

    # Render header
    render_header()

    # Render search section
    render_search_section()

    # Render featured artists
    render_featured_artists()

    # Horizontal divider
    st.markdown("<hr style='margin: 30px 0; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

    # Render analysis results
    render_analysis_results()

    # Render sidebar
    render_sidebar()


if __name__ == "__main__":
    main()
