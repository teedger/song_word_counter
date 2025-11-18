# 🏗️ Architecture Overview

This document explains the architecture and design decisions of the Artist Lyrics Analyzer.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                      (Streamlit App)                         │
│                     frontend/app.py                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─────────────────┐
                     ▼                 ▼
         ┌───────────────────┐  ┌──────────────────┐
         │  Visualization    │  │   Analysis       │
         │     Module        │  │    Module        │
         │ visualizations.py │  │  analyzer.py     │
         └───────────────────┘  └────────┬─────────┘
                                         │
                     ┌───────────────────┼────────────────┐
                     ▼                   ▼                ▼
         ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
         │ Text Processor   │  │   Lyrics     │  │    Cache     │
         │ text_processor.py│  │   Fetcher    │  │   Manager    │
         │                  │  │lyrics_fetcher│  │cache_manager │
         └──────────────────┘  └──────┬───────┘  └──────┬───────┘
                                      │                  │
                                      ▼                  ▼
                              ┌──────────────┐  ┌──────────────┐
                              │  Genius API  │  │ Local Cache  │
                              │   (External) │  │  (data/)     │
                              └──────────────┘  └──────────────┘
```

## Component Breakdown

### 1. Frontend Layer

#### `frontend/app.py` - Main Application
- **Purpose**: User interface and interaction
- **Technology**: Streamlit
- **Responsibilities**:
  - Render UI components
  - Handle user input
  - Coordinate between modules
  - Display results
  - Manage session state

#### `frontend/visualizations.py` - Visualization Module
- **Purpose**: Create charts and visual representations
- **Technology**: Plotly, WordCloud, Matplotlib
- **Responsibilities**:
  - Generate word clouds
  - Create interactive charts
  - Build comparison graphs
  - Design timeline visualizations
  - Apply music-inspired styling

### 2. Backend Layer

#### `backend/lyrics_fetcher.py` - Lyrics Fetcher
- **Purpose**: Retrieve lyrics from Genius API
- **Technology**: lyricsgenius library
- **Responsibilities**:
  - Authenticate with Genius API
  - Search for artists
  - Fetch song lyrics
  - Clean raw lyrics data
  - Handle rate limiting
  - Coordinate with cache manager

**Flow**:
```
User Request → Check Cache → Cache Hit? → Return Cached Data
                    ↓ No
              Fetch from API → Clean Data → Save to Cache → Return Data
```

#### `backend/text_processor.py` - Text Processor
- **Purpose**: Process and clean lyrics text
- **Technology**: NLTK
- **Responsibilities**:
  - Tokenize text into words
  - Remove stop words
  - Filter invalid words
  - Clean punctuation
  - Calculate word frequencies
  - Generate unique word sets

**Processing Pipeline**:
```
Raw Lyrics
    ↓
Tokenization (split into words)
    ↓
Cleaning (remove punctuation, lowercase)
    ↓
Filtering (remove stop words, short words)
    ↓
Validation (alpha characters only)
    ↓
Processed Words
```

#### `backend/analyzer.py` - Lyrics Analyzer
- **Purpose**: Perform statistical analysis
- **Technology**: Pandas, NumPy
- **Responsibilities**:
  - Analyze artist's entire catalog
  - Calculate vocabulary diversity
  - Generate top word lists
  - Compute per-song statistics
  - Create comparison data
  - Build timeline data

**Analysis Metrics**:
- **Unique Words**: Total distinct words across all songs
- **Total Words**: Sum of all processed words
- **Diversity Score**: Ratio of unique/total words (scaled 0-10)
- **Frequency Distribution**: Word usage counts
- **Per-Song Stats**: Individual song analysis

#### `backend/cache_manager.py` - Cache Manager
- **Purpose**: Manage local data caching
- **Technology**: JSON file storage
- **Responsibilities**:
  - Save fetched data
  - Retrieve cached data
  - Check cache validity
  - Manage expiration
  - Clear cache

**Cache Structure**:
```json
{
  "artist_name": "Artist Name",
  "cached_at": "2024-01-01T12:00:00",
  "data": {
    "total_songs": 50,
    "songs": [...],
    ...
  }
}
```

### 3. Configuration Layer

#### `config.py` - Configuration Settings
- **Purpose**: Centralized configuration
- **Contents**:
  - API settings
  - Cache configuration
  - Stop words list
  - Color palette
  - Featured artists
  - Analysis parameters

## Data Flow

### Complete Analysis Flow

```
1. User enters artist name
        ↓
2. App checks cache
        ↓
3. If not cached:
   a. Fetch lyrics from Genius API
   b. Clean and process text
   c. Save to cache
        ↓
4. Text Processor analyzes lyrics
        ↓
5. Analyzer calculates statistics
        ↓
6. Visualizer creates charts
        ↓
7. Results displayed to user
```

### Caching Strategy

```
Request Artist Data
        ↓
    Is Cached? ──Yes──> Is Fresh? ──Yes──> Return Cache
        │                   │
       No                  No
        │                   │
        └───────────────────┘
                    ↓
            Fetch from API
                    ↓
            Process & Save
                    ↓
            Return Data
```

## Design Patterns

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Frontend handles UI, Backend handles data
- Clean interfaces between components

### 2. **Caching Pattern**
- Transparent caching layer
- Automatic expiration
- Reduces API calls and improves performance

### 3. **Pipeline Pattern**
- Text processing follows a clear pipeline
- Each step transforms data for the next
- Easy to extend with new processing steps

### 4. **Strategy Pattern**
- Different visualization strategies
- Pluggable analysis methods
- Easy to add new chart types

## Performance Optimizations

### 1. **Caching**
- Cache lyrics for 30 days (configurable)
- Avoid redundant API calls
- Instant results for cached artists

### 2. **Rate Limiting**
- Respect Genius API limits
- Configurable delay between requests
- Prevent throttling

### 3. **Batch Processing**
- Process all songs together
- Single pass frequency counting
- Efficient memory usage

### 4. **Lazy Loading**
- Download NLTK data on-demand
- Load visualizations only when needed
- Progressive rendering

## Security Considerations

### 1. **API Token Management**
- Tokens stored in .env file (not in code)
- .env excluded from git
- Environment variables for sensitive data

### 2. **Input Validation**
- Sanitize user input
- Validate artist names
- Prevent injection attacks

### 3. **Error Handling**
- Graceful failure
- User-friendly error messages
- No sensitive data in errors

## Extensibility Points

### Easy to Extend

1. **Add New Visualizations**
   - Add methods to `visualizations.py`
   - Call from `app.py`

2. **Add New Analysis Metrics**
   - Extend `analyzer.py`
   - Update UI to display new metrics

3. **Support New Data Sources**
   - Create new fetcher class
   - Implement same interface
   - Swap in `app.py`

4. **Add New Text Processing**
   - Extend `text_processor.py`
   - Add to processing pipeline
   - Configure in `config.py`

## Technology Choices

### Why Streamlit?
- ✅ Rapid development
- ✅ Beautiful default UI
- ✅ Built-in state management
- ✅ Easy deployment
- ✅ Python-native (no JS needed)

### Why Plotly?
- ✅ Interactive charts
- ✅ Professional appearance
- ✅ Easy customization
- ✅ Good Streamlit integration

### Why NLTK?
- ✅ Mature NLP library
- ✅ Comprehensive tools
- ✅ Well-documented
- ✅ Good tokenization

### Why JSON for Cache?
- ✅ Human-readable
- ✅ Easy to debug
- ✅ No database needed
- ✅ Portable

## Future Enhancements

### Potential Improvements

1. **Database Backend**
   - SQLite or PostgreSQL
   - Better query performance
   - Relational data

2. **Real-time Collaboration**
   - Multiple users
   - Shared analyses
   - Social features

3. **Advanced Analytics**
   - Sentiment analysis
   - Rhyme pattern detection
   - Collaboration network

4. **Export Features**
   - PDF reports
   - CSV data export
   - Shareable links

5. **Playlist Integration**
   - Spotify API integration
   - Analyze playlists
   - Discover similar artists

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Document functions
- Keep functions small

### Testing
- Unit tests for each module
- Integration tests for workflows
- Test with various artists

### Documentation
- Clear docstrings
- README for users
- ARCHITECTURE for developers
- Inline comments for complex logic

---

**Last Updated**: November 2024
**Version**: 1.0.0
