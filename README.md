# Lyrics-Web-Scraper

## 1. WebScrape.py - Utilities to collect lyrics from wikia.com 
lyricsFromSongs() takes in a list of song urls and returns the lyrics.

song_urls() collects the urls for a list of albums urls. These come back for wikia pretty course so the helper function sortUrls can be used to clean them up.

album_urls() collects the urls for a list of genre urls.

processSongs breaks a list of song urls into batches, write the lyrics for them to a file.
Collecting large lists via BeautifulSoup takes time so batches are written to files.

Example Usage: lyricsByGenre.py, lyricsByArtist.py

### Resources:
[My Google Doc Notes](https://docs.google.com/document/d/1t_rl6RX3gDJDjWde95zKfq8gICQojKssXN9buWS1sZk/edit?usp=sharing)
General web scraping notes for Galvanize course: https://github.com/sagecodes/intro-web-scraping

## 2. AnalyzeLyrics.py - A script that loads lyrics saved from the above and prints a report.
- Size of the lyric data loaded: number of songs, phrases, words etc.
- Average number of words and characters per phrase and song.
- Distributions of words, bigrams ...

![Words Distribution](https://github.com/ROB1NSON/Lyrics-Web-Scraper/blob/master/American_Folk-Part_dist_words.png)

![Trigrams Distribution](https://github.com/ROB1NSON/Lyrics-Web-Scraper/blob/master/American_Folk-Part_dist_trigrams.png)

[//]: # (## Next steps)
[//]: # (Generate song lyrics.  Consider constraining via forcing rhyming words every 1.5 phrases. Forward - Backward RNN)
