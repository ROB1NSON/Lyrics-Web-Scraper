from WebScrape import *

# http://lyrics.wikia.com/wiki/Category:Song
# http://lyrics.wikia.com/wiki/Category:Language/English
#genre = 'Folk'
genre = 'American_Folk'

genreUrls = ['http://lyrics.wikia.com/wiki/Category:Genre/{}'.format(genre)]
albumsFile = 'data/albums-genre-{}.yml'.format(genre)
#os.remove(albumsFile)
if os.path.isfile(albumsFile):
    with open(albumsFile, 'r') as f:
        albumUrls = yaml.safe_load(f)
else:
    albumUrls = album_urls(genreUrls)
    with open(albumsFile, 'w') as f:
        yaml.safe_dump(albumUrls, f)

#albumUrls = ['http://lyrics.wikia.com/wiki/Emry_Arthur', 'http://lyrics.wikia.com/wiki/Aiken_County_String_Band', 'http://lyrics.wikia.com/wiki/A_Nod_To_Bob_(2001)']
#songUrls = song_urls(albumUrls)
songsFile = 'data/songs-{}.yml'.format(genre)

#os.remove(songsFile)
if os.path.isfile(songsFile):
    with open(songsFile, 'rb') as f:
        songUrls = yaml.safe_load(f)
else:
    songUrls_course = song_urls(albumUrls)
    songUrls0, extraAlbums = sortUrls(songUrls_course)
    songUrls_course2 = song_urls(extraAlbums)
    songUrls2, extraAlbums2 = sortUrls(songUrls_course2)

    songUrls = songUrls0 + songUrls2

    #No. songUrls0: 21660
    #No. songUrls2: 55504
    #No. extra albums: 1152
    #No. extra albums2: 499
    print('No. songUrls0: {}'.format(len(songUrls0)))
    print('No. songUrls2: {}'.format(len(songUrls2)))
    print('No. extra albums: {}'.format(len(extraAlbums)))
    print('No. extra albums2: {}'.format(len(extraAlbums2)))

    songUrls = list(sorted(set(songUrls)))

    with open(songsFile, 'w') as f:
        yaml.safe_dump(songUrls, f)

    with open(albumsFile, 'w') as f:
        yaml.safe_dump(albumUrls+extraAlbums+extraAlbums2, f)

#songUrls = ['http://lyrics.wikia.com/wiki/Emry_Arthur:Man_Of_Constant_Sorrow', 'http://lyrics.wikia.com/wiki/Alison_Krauss_%26_Union_Station:I_Am_A_Man_Of_Constant_Sorrow']

processSongs(songsFile, genre=genre)
