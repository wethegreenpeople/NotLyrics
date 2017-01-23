import markovify
import requests
import bs4
import os.path


def ArtistSongs(artist, i):
	response = requests.get('http://www.songlyrics.com/' + artist + '-lyrics/')
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	result = soup.find_all("a", {"itemprop":"url"})
	return result[i].get('href')
	
def SaveLyrics(artist, song):
	response = requests.get(song)
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	result = soup.find("p", {"id":"songLyricsDiv"}).text.encode('utf-8')
	with open('lyrics/' + artist + '.txt', 'a') as file:
		file.write(str(result))

def FixLyrics(artist):
	with open('lyrics/' + artist + '.txt', 'r') as src:
		with open('lyrics/fixed/' + artist + 'f.txt', 'w') as dest:
			for line in src:
				if line.endswith(",") is False:
					dest.write('%s%s\n' % (line.strip(), '.'))
				else:
					line = line[:-1]
					dest.write('%s%s\n' % (line.strip(), '.'))

def GenerateLyric(artist):
	if (os.path.isfile('lyrics/' + artist + '.txt') == True):
		FixLyrics(artist)
		with open('lyrics/fixed/' + artist + 'f.txt') as f:
			text = f.read()
			text_model = markovify.Text(text)
			return text_model.make_sentence()
	else:
		for i in range(0,25):
			SaveLyrics(artist, ArtistSongs(artist, i))
			FixLyrics(artist)
		return "None"