import os
import yaml
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup, element

# Utilities to collect lyrics from wikia.com.
#


def lyricsFromSongs(song_urls):
    # Return a list of "songs"
    #  - a song is list or strings. The first is the url followed by "phrases" - a phrase is a string of words.
    #  Example input: 'http://lyrics.wikia.com/wiki/Alison_Krauss_%26_Union_Station:I_Am_A_Man_Of_Constant_Sorrow'
    lyrics = []
    for songUrl in song_urls:
        if 'comhttp' in songUrl:
            continue
        print('getting lyrics for: {}'.format(songUrl))
        r = requests.get(songUrl)
        c = r.content
        soup = BeautifulSoup(c)
        main_contents = soup.find_all('div', attrs={'class': 'lyricbox'})
        # get the songs on this page
        for contents in main_contents:
            theseLyrics = [songUrl]
            for content in contents.contents:
                #< div class ="lyricbox" > I am a man of constant sorrow < br > I'v' ...
                #        'olden shore)<div class="lyricsbreak"></div>
                if type(content) != element.Tag:
                    #theseLyrics = ' <br> '.join([theseLyrics, content])
                    theseLyrics += ['{}'.format(content)]
            lyrics.append(theseLyrics)

    return lyrics


def album_urls(genre_urls):
    # Example input: 'http://lyrics.wikia.com/wiki/Category:Genre/American_Folk'
    album_hrefs = []
    for genreUrl in genre_urls:
        o = urlparse(genreUrl)
        while genreUrl:
            r = requests.get(genreUrl)

            # use BeautifulSoup on content from request
            c = r.content
            soup = BeautifulSoup(c)
            # pretty_soup = soup.prettify()

            # get elements within the 'main-content' tag
            # main_content = soup.find('div', attrs={'class': 'category-page__members'})
            # main_content = soup.find_all('div', attrs = {'class': 'category-page__first-char'})
            main_content = soup.find_all('a', attrs={'class': 'category-page__member-link'})

            # get the album links on this page
            # album_titles = [content.text for content in main_content]
            album_hrefs += ['{}://{}{}'.format(o.scheme, o.netloc, content.attrs['href']) for content in main_content]

            pagination = soup.find('div', attrs={'class': 'category-page__pagination'})
            # get the Next Button link
            genreUrl = None
            for content in pagination.contents:
                if hasattr(content, 'text'):
                    if 'Next' in content.text:
                        genreUrl = content.attrs['href']
                        break

    return album_hrefs


def song_urls(album_urls):
    # Example input: 'http://lyrics.wikia.com/wiki/Alison_Krauss_%26_Union_Station'
    song_hrefs = []
    for albumUrl in album_urls:
        print('album url: {}'.format(albumUrl))
        o = urlparse(albumUrl)
        r = requests.get(albumUrl)
        c = r.content
        soup = BeautifulSoup(c)

        # get the songs on this page
        #main_contents = soup.find_all('ol')
        main_contents = soup.find('div', attrs={'class': 'mw-content-ltr'})

            # Get all links(a) in the main_content div.
            # for each link in list print link text and the link URL(href)
            #content = main_content.find_all('a')
            #for link in content:
            #    print("\n" + link.text + ":")
            #    print(link['href'])
        for mc in main_contents:
            if mc.find('li') and type(mc) == element.Tag:
                for li in mc.contents:
                    if type(li) == element.Tag:
                        for content in li.contents:
                            if type(content) == element.Tag:
                                for cont in content:
                                  if type(cont) == element.Tag and 'href' in cont.attrs.keys():
                                    song_hrefs += ['{}://{}{}'.format(o.scheme, o.netloc, cont.attrs['href'])]
                                    for c in cont:
                                        if type(c) == element.Tag and 'href' in c.attrs.keys():
                                            song_hrefs += ['{}://{}{}'.format(o.scheme, o.netloc, c.attrs['href'])]

    return song_hrefs


def sortUrls(songUrls):
    # Some urls found on a page expected to contain songs (album pages) contain more albums
    lessSongs = []
    extraAlbums = []
    for url in songUrls:
        if ':' in url[5:]:
            lessSongs.append(url)
        else:
            extraAlbums.append(url)
    return lessSongs, extraAlbums


def processSongs(songsFileName, genre=None):
    # break list into pieces, init from log file, get lyrics for each piece, append piece to whole, rewrite file, write log file
    if not genre:
        #get genre from songFileName
        raise

    totalLyricsFile = 'data/lyrics-{}.yml'.format(genre)

    with open(songsFileName, 'r') as song_in:
        songUrls = yaml.safe_load(song_in)

    # Break out batches
    numSongs = len(songUrls)
    batchSize = min(3000, numSongs)
    batchIncrements = [r for r in range(0, numSongs, batchSize)] + [numSongs]
    batches = zip(batchIncrements, batchIncrements[1:])

    for i, batch in enumerate(batches):
        thisLyricsFile = 'data/lyrics-{}-{}.yml'.format(genre, i)

        # Look to see if we have been this far before
        if os.path.isfile(thisLyricsFile):
            continue

        lyrics = lyricsFromSongs(songUrls[batch[0]:batch[1]])

        with open(thisLyricsFile, 'w') as some_lyrics_out:
            yaml.dump(lyrics, some_lyrics_out)
        print('Wrote', len(lyrics), 'song lyrics to', thisLyricsFile)

        previousLyrics = []
        if os.path.isfile(totalLyricsFile):
            with open(totalLyricsFile, 'r') as lyrics_in:
                previousLyrics = yaml.load(lyrics_in)

        with open(totalLyricsFile, 'w') as all_lyrics_out:
                yaml.dump(previousLyrics+lyrics, all_lyrics_out)

    print('Wrote', totalLyricsFile)

"""
# https://medium.com/@Alexander_H/scraping-wikipedia-with-python-8000fc9c9e6c
import wikipedia
wikipedia.set_lang("en")
query = ''
WikiPage = wikipedia.page(title = query,auto_suggest = True)
cat = WikiPage.categories
"""