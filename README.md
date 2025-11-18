# 🎵 Artist Lyrics Analyzer

A beautiful, music-inspired web application that analyzes the lyrical vocabulary and diversity of your favorite artists. Built with Python, Streamlit, and powered by the Genius API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 🎤 **Artist Search** - Search and analyze any artist on Genius
- 📊 **Comprehensive Analysis** - Unique word counts, vocabulary diversity scores, and detailed statistics
- 📈 **Beautiful Visualizations**
  - Interactive word clouds
  - Top words bar charts
  - Vocabulary diversity gauges
  - Timeline evolution graphs
- 💾 **Smart Caching** - Automatically caches results to minimize API calls
- 🎨 **Music-Inspired Design** - Dark theme with neon gradients and smooth animations
- 🎯 **Featured Artists** - Quick access to popular artists

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Genius API token (free - [get yours here](https://genius.com/api-clients))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd song_word_counter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API token**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your Genius API token
   # GENIUS_API_TOKEN=your_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run frontend/app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 🎯 How to Use

1. **Search for an Artist**
   - Enter an artist name in the search bar
   - Adjust the maximum number of songs to analyze (10-200)
   - Click "Analyze"

2. **Explore Featured Artists**
   - Click on any featured artist button for instant analysis

3. **View Results**
   - Vocabulary diversity score (0-10)
   - Total unique words across all songs
   - Most frequently used words
   - Interactive visualizations
   - Timeline of vocabulary evolution

4. **Compare Artists**
   - Analyze multiple artists
   - Compare their vocabulary diversity and unique word counts

## 📁 Project Structure

```
song_word_counter/
├── backend/
│   ├── lyrics_fetcher.py      # Genius API integration
│   ├── text_processor.py      # Text tokenization & cleaning
│   ├── analyzer.py             # Statistical analysis
│   └── cache_manager.py        # Caching system
├── frontend/
│   ├── app.py                  # Main Streamlit app
│   └── visualizations.py       # Plotly charts & graphs
├── data/
│   ├── cache/                  # Cached lyrics data
│   └── preloaded/              # Pre-analyzed artists
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md
```

## 🛠️ Technology Stack

### Core
- **Streamlit** - Web application framework
- **lyricsgenius** - Genius API wrapper
- **NLTK** - Natural language processing
- **Pandas** - Data manipulation

### Visualization
- **Plotly** - Interactive charts
- **WordCloud** - Word cloud generation
- **Matplotlib** - Additional visualizations

### Utilities
- **python-dotenv** - Environment variables
- **tqdm** - Progress bars
- **SQLAlchemy** - Data storage

## ⚙️ Configuration

Edit `config.py` to customize:

- **Cache settings** - Cache expiry duration
- **Analysis settings** - Minimum word length, max songs per artist
- **Stop words** - Words to exclude from analysis
- **Color palette** - Customize the visual theme
- **Featured artists** - Pre-loaded artist list

## 📊 How It Works

1. **Lyrics Fetching**
   - Connects to Genius API
   - Fetches artist's songs sorted by popularity
   - Caches results for 30 days

2. **Text Processing**
   - Tokenizes lyrics into individual words
   - Removes stop words (prepositions, articles, etc.)
   - Filters out song structure markers ([Chorus], [Verse], etc.)
   - Cleans punctuation and special characters

3. **Analysis**
   - Counts unique words across all songs
   - Calculates word frequency
   - Computes vocabulary diversity score
   - Generates per-song statistics

4. **Visualization**
   - Creates interactive Plotly charts
   - Generates word clouds with music-inspired design
   - Displays statistics in beautiful gradient cards

## 🎨 Design Philosophy

The application features a **music-inspired aesthetic** with:
- Dark navy background (`#0a0e27`)
- Hot pink primary color (`#ff006e`)
- Purple secondary color (`#8338ec`)
- Neon green accents (`#06ffa5`)
- Smooth gradients and animations
- Responsive, modern layout

## 📝 Notes

- **API Rate Limiting**: The app respects Genius API rate limits with automatic delays between requests
- **Cache Management**: Clear the cache from the sidebar to fetch fresh data
- **Privacy**: All analysis is done locally; no data is sent to third parties
- **Copyright**: This tool analyzes lyrics statistically and does not reproduce full copyrighted content

## 🔑 Getting Your Genius API Token

1. Go to [https://genius.com/api-clients](https://genius.com/api-clients)
2. Sign in or create a free account
3. Click "New API Client"
4. Fill in the application details (name, description, etc.)
5. Copy your "Client Access Token"
6. Add it to your `.env` file

## 🐛 Troubleshooting

**"API token not found" error**
- Make sure you created a `.env` file in the project root
- Check that `GENIUS_API_TOKEN` is set correctly
- Restart the application

**"Artist not found" error**
- Try different spellings or variations of the artist name
- Some artists may not be available on Genius

**Slow performance**
- Reduce the maximum number of songs to analyze
- Check your internet connection
- Clear the cache and try again

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Genius API** for providing lyrics data
- **Streamlit** for the amazing web framework
- **NLTK** for natural language processing tools

---

Made with ❤️ and 🎵 for music lovers and data enthusiasts
