# NotLyrics
NotLyrics is a Python program to test out Markov chains. When an artist is given to the program, it will download the lyrics, and then generate a fake lyric based out of the composistion of the real lyrics for the artist. 

You can see a very rough example of the program in action at: http://uraqt.xyz/notlyrics

This project was made possibly largely because of the markovify library: https://github.com/jsvine/markovify, and http://www.songlyrics.com/

NotLyrics will eventually download all of an artist's songs, so as to have a bigger library of text to make sentences out of. The first time that an artist is requested it will download 20 songs. Then if the same artist is requested 30 minutes later it'll request another 5, until all of the songs have been downloaded. I don't want to hammer the Lyrics website with requests, but I found that on average 20 songs is where you start getting new/interesting sentences. So I thought this was a fair enough compromise.