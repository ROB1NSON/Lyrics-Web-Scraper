import yaml
import numpy as np
import syllables
import matplotlib.pyplot as plt

HOME_DIR = './'

genre = 'American_Folk-Part'

def get_lyrics(genre='American_Folk', n_songs=None):
    #songsFile = 'data/songs-{}.yml'.format(genre)
    #with open(songsFile, 'r') as f:
    #    songUrls = yaml.load(f)
    #print(len(songUrls))

    # Load full lyrics file and select every 30th - to limit the data for debugging
    # One file with 3k lyricSets fills 10% memory to plot word popularity distribution (8 GB machine)
    lyricsFile = HOME_DIR + 'data/lyrics-{}.yml'.format(genre)
    with open(lyricsFile, 'r') as f:
        allLyrics = yaml.load(f)

    # Return the number of songs
    # Need a faster way to count all the words - for now just look at 500 songs
    n_keep = min(n_songs, len(allLyrics))
    n_rate = int(len(allLyrics) / n_keep)
    return [allLyrics[r] for r in range(0, len(allLyrics), n_rate)]


lyrics = get_lyrics(genre=genre, n_songs=1000)
# TODO check if song is in English
#   http://lyrics.wikia.com/wiki/Antonio_Carlos_Jobim:She%27s_A_Carioca
# TODO check if lyricSet is sane; e.g. '?' or '_____'
#   http://lyrics.wikia.com/wiki/Category:Partial_Lyrics

title_format = '{} Distribution (based on {} {})'

#
def plotTokenDistribution(tokens, sortByPopularity=True):
    # Input a list of strings, count their relative contributions: words, bigrams, ...
    # Probably an okay pythonic way to count but the large list needs to be a db object
    popularity = {}
    for token in list(set(tokens)):
        popularity[token] = tokens.count(token) / len(tokens)

    if sortByPopularity:
        pop_listoftups = [(w, popularity[w]) for w in sorted(popularity, key=popularity.get, reverse=True)]
        x_vals, y_vals = zip(*pop_listoftups)  # convert to lists
    else:  # sort by alpha-number
        x_vals = sorted(popularity.keys())
        y_vals = [popularity[x] for x in x_vals]

    fig, ax = plt.subplots()

    ax.plot(x_vals[:20], y_vals[:20], 'x')
    if isinstance(x_vals[0], str):
        ax.set_xticklabels(x_vals[:20], rotation=45, horizontalalignment='right')
    ax.grid(b=True)

    return fig


## Most common words
findCommonWords = True
if findCommonWords:
    words = [w.lower() for lyricSet in lyrics for phrase in lyricSet[1:] for w in phrase.split()]
    fig_words = plotTokenDistribution(words)
    fig_words.axes[0].axes.set_title(title_format.format('Words', len(words), 'words'))
    fig_words.show()
    fig_words.savefig('{}_dist_words.png'.format(genre))

## Most popular bigrams
findCommonBigrams = True
if findCommonBigrams:
    bigrams = []
    for lyricSet in lyrics:
        for phrase in lyricSet[1:]:
            words = phrase.lower().split()
            if any([word.isalpha() for word in words]):
                words = ['<s>'] + words + ['</s>']
                bigrams += [' '.join([b[0], b[1]]) for b in zip(words, words[1:])]

    fig_bigrams = plotTokenDistribution(bigrams)
    fig_bigrams.axes[0].set_title(title_format.format('Bigrams', len(bigrams), 'bigrams'))
    fig_bigrams.show()
    fig_bigrams.savefig('{}_dist_bigrams.png'.format(genre))

## Most popular trigrams
findCommonTrigrams = True
if findCommonTrigrams:
    trigrams = []
    for lyricSet in lyrics:
        for phrase in lyricSet[1:]:
            words = phrase.lower().split()
            if any([word.isalpha() for word in words]):
                words = ['<s>'] + words + ['</s>']
                trigrams += [' '.join([b[0], b[1], b[2]]) for b in zip(words, words[1:], words[2:])]

    fig_trigrams = plotTokenDistribution(trigrams)
    fig_trigrams.axes[0].set_title(title_format.format('Trigrams', len(trigrams), 'trigrams'))
    fig_trigrams.show()
    fig_trigrams.savefig('{}_dist_trigrams.png'.format(genre))

# Distribution of syllables per phrase
# Using PyPI syllables  (TODO compare Pyphen)
analyzeSyllables = True
if analyzeSyllables:
    syls = [syllables.estimate(phrase) for song in lyrics for phrase in song[1:]]
    fig_syllables = plotTokenDistribution(syls, sortByPopularity=False)
    fig_syllables.axes[0].set_title(title_format.format('Syllables', len(syls), 'syllables'))
    fig_syllables.show()
    fig_syllables.savefig('{}_dist_syllables.png'.format(genre))

# Number of songs in the genre
n = len(lyrics)
print('{} songs in {}'.format(n, genre))
print('')

# Phrases, words, and characters per song, phrase, ...
songs_by_phrases = []
songs_by_words = []
songs_by_characters = []
phrases_by_words = []
phrases_by_characters = []
for song in lyrics:
    phrases = []
    for phrase in song[1:]:
        if not phrase == '\n':  # break in Verse/Chorus
            phrases.append(phrase.replace('\n', ''))
            phrases_by_words.append([w for w in phrase.split()])
            phrases_by_characters.append([c for w in phrase.split() for c in w])
    songs_by_phrases.append(phrases)
    songs_by_words.append([w for phrase in phrases for w in phrase.split()])
    songs_by_characters.append([c for phrase in phrases for c in phrase])

# Number of phrases (total and per song)
nPhrases_per_song = [len(songPhrases) for songPhrases in songs_by_phrases]
print('{:10,} phrases total'.format(sum(nPhrases_per_song)))
print('Number of phrases per song: {:.2f} +/- {:.2f}'.format(np.mean(nPhrases_per_song), np.std(nPhrases_per_song)))
print('')

# Number of words per phrase
nWords_per_phrase = [len(phraseWords) for phraseWords in phrases_by_words]
print('{:10,} words total'.format(sum(nWords_per_phrase)))
print('Number of words per phrase: {:.2f} +/- {:.2f}'.format(np.mean(nWords_per_phrase), np.std(nWords_per_phrase)))
print('')

# Number of syllables per phrase:  9 +/- 5 in American Folk
nSyls_per_phrase = [syllables.estimate(phrase) for songPhrases in songs_by_phrases for phrase in songPhrases]
print('{:10,} syllables total'.format(sum(nSyls_per_phrase)))
print('Number of syllables per phrase: {:.2f} +/- {:.2f}'.format(np.mean(nSyls_per_phrase), np.std(nSyls_per_phrase)))
print('')

# Number of characters per phrase, per song
nChars_per_song = [len(chars) for chars in songs_by_characters]
print('{:10,} characters total'.format(sum(nChars_per_song)))  # 34M in American Folk
print('Number of characters per song: {:.2f} +/- {:.2f}'.format(np.mean(nChars_per_song), np.std(nChars_per_song)))

nChars_per_phrase = [len(phraseChars) for phraseChars in phrases_by_characters]
print('Number of characters per phrase: {:.2f} +/- {:.2f}'.format(np.mean(nChars_per_phrase), np.std(nChars_per_phrase)))

# Properties of phrases - relative to prior / next prior
# Most popular first 3 words when first word is capitalized
