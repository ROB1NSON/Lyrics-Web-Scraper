
## 1. WebScrape.py - Utilities to collect lyrics from wikia.com 
lyricsFromSongs() takes in a list of song urls and returns the lyrics.

song_urls() collects the urls for a list of albums urls. These come back for wikia pretty course so the helper function sortUrls can be used to clean them up.

album_urls() collects the urls for a list of genre urls.

processSongs breaks a list of song urls into batches, write the lyrics for them to a file.
Collecting large lists via BeautifulSoup takes time so batches are written to files.

Example Usage: lyricsByGenre.py, lyricsByArtist.py

### Resources:
General web scraping notes for Galvanize course: https://github.com/sagecodes/intro-web-scraping

## 2. AnalyzeLyrics.py - A script that loads lyrics saved from the above and prints a report.
- Size of the lyric data loaded: number of songs, phrases, words etc.
- Average number of words and characters per phrase and song.
- Distributions of words, bigrams ...

[//]: # (## Next steps)
[//]: # (Generate song lyrics.  Consider constraining via forcing rhyming words every 1.5 phrases. Forward - Backward RNN)

