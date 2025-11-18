# 🚀 Quick Start Guide

Get up and running with the Artist Lyrics Analyzer in 3 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- lyricsgenius (API wrapper)
- plotly (visualizations)
- NLTK (text processing)
- and other dependencies

## Step 2: Get Your Genius API Token

1. Visit [https://genius.com/api-clients](https://genius.com/api-clients)
2. Sign in or create a free account
3. Click **"New API Client"**
4. Fill in:
   - **App Name**: "My Lyrics Analyzer" (or any name)
   - **App Website URL**: http://localhost (or your website)
5. Click **"Save"**
6. Copy your **"Client Access Token"**

## Step 3: Configure Your Token

```bash
# Copy the example file
cp .env.example .env

# Edit .env and paste your token
# GENIUS_API_TOKEN=paste_your_token_here
```

Or manually create `.env` file:
```
GENIUS_API_TOKEN=your_actual_token_here
```

## Step 4: Run the App

```bash
# Easy way - using the run script
python run.py

# Or manually
streamlit run frontend/app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Step 5: Analyze Your First Artist

1. Type an artist name in the search bar (e.g., "Rihanna")
2. Click **"Analyze"**
3. Wait while it fetches and analyzes lyrics
4. Explore the beautiful visualizations!

## 🎯 Pro Tips

### Quick Access to Featured Artists
Click on any featured artist button for instant analysis

### Adjust Number of Songs
Use the "Max Songs" field to analyze more or fewer songs (10-200)

### Pre-load Common Artists
Run this to cache popular artists for faster access:
```bash
python preload_artists.py
```

### Clear Cache
If you want fresh data, click "Clear Cache" in the sidebar

## 🧪 Test Your Setup

Run the test script to verify everything is working:
```bash
python test_basic.py
```

## 📊 What You'll See

- **Vocabulary Diversity Score** (0-10) - How varied the artist's vocabulary is
- **Unique Words Count** - Total number of unique words used
- **Top Words Chart** - Most frequently used words
- **Word Cloud** - Visual representation of word frequencies
- **Timeline** - How vocabulary evolved over the years
- **Detailed Statistics** - Per-song breakdowns and more

## ⚙️ Customization

Edit `config.py` to customize:
- Stop words (words to exclude)
- Color scheme
- Featured artists list
- Cache duration
- And more!

## 🐛 Common Issues

**"API token not found"**
- Make sure `.env` file exists in the project root
- Check that the token is on a line: `GENIUS_API_TOKEN=your_token`
- No quotes needed around the token

**"ModuleNotFoundError"**
- Run: `pip install -r requirements.txt`
- Make sure you're in the project directory

**"Artist not found"**
- Try different spellings
- Check if the artist exists on Genius.com
- Some artists may have limited data

**App is slow**
- Reduce max songs to 20-30 for faster results
- First run takes longer (building cache)
- Subsequent searches for the same artist are instant!

## 🎉 You're Ready!

Enjoy analyzing the lyrical vocabulary of your favorite artists!

---

**Need help?** Check out the full [README.md](README.md) for more details.
