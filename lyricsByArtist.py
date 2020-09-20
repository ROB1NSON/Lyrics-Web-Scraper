import yaml
from WebScrape import song_urls, processSongs

artist = 'The_Residents'

artistUrls = ['http://lyrics.wikia.com/wiki/{}'.format(artist)]

# Collect the list of song urls
songUrls_course = song_urls(artistUrls)
songUrls = list(sorted(set(songUrls_course)))

songsFile = 'songs_by_{}_urls.yml'.format(artist)
with open(songsFile, 'w') as f:
    yaml.safe_dump(songUrls, f)

processSongs(songsFile, genre=artist)
