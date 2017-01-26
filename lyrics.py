import markovify
import requests
import bs4
import os.path
import time

startSong = 0
endSong = 3
maxSong = 0

def ArtistSongs(artist, i):
	response = requests.get('http://www.songlyrics.com/' + artist + '-lyrics/')
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	result = soup.find_all("a", {"itemprop":"url"})
	return result[i].get('href')
	
def SaveLyrics(artist, song, endSong):
	response = requests.get(song)
	soup = bs4.BeautifulSoup(response.text, "html.parser")
	result = soup.find("p", {"id":"songLyricsDiv"}).get_text()
	with open('lyrics/' + artist + '.txt', 'a+') as file:
		file.write(str(result))
	with open('lyrics/' + artist + '.txt', 'r+') as file:
		file.write(str(endSong) + "," + str(time.time()) + "\n")

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
	lyricPath = 'lyrics/' + artist + '.txt'
	lyricfPath = 'lyrics/fixed/' + artist + 'f.txt'
	# File exists?
	if (os.path.isfile(lyricPath) == True):
		with open(lyricPath) as f:
			doot = f.readline().split(',')
			startSong = int(doot[0])
			lastTime = float(doot[1])
		endSong = startSong + 5
		# If it's been more than 15 minutess
		if (time.time() >= lastTime + 900):
			maxSong = len(ArtistSongs(artist, 0))
			# If we haven't downloaded all the available song
			if (startSong < maxSong):
				for i in range(startSong, endSong):
					SaveLyrics(artist, ArtistSongs(artist, i), endSong)
		else:
			print("Sorry mang, you have to wait before downloading more songs from this artist")
		FixLyrics(artist)
		with open(lyricfPath) as f:
			text = f.read()
			text_model = markovify.Text(text)
		return text_model.make_sentence()
	# If the artist has never been requested before
	else:
		for i in range(0, 20):
			SaveLyrics(artist, ArtistSongs(artist, i), 20)
		FixLyrics(artist)
		with open(lyricfPath) as f:
			text = f.read()
			text_model = markovify.Text(text)
		return text_model.make_sentence()