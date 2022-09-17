import yt_dlp as youtube_dl
import os
from requests import get
import html
import re
import eyed3

def main():
    '''
    https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
    '''
    # okay, it knows where it is when run
    Album_Name = os.getcwd()[::-1].split('/')[0][::-1]
    Artist_Name = os.getcwd()[::-1].split('/')[1][::-1]

    # let's search discogs for this to find the songs in this album
    # assemble a discogs search string
    search_string = Album_Name + ' ' + Artist_Name
    search_string = search_string.replace(' ','+').replace('_','+')
    search_string = 'https://www.discogs.com/search/?q=' + search_string + '&type=all'

    # get discogs search results
    search_results = get(search_string).text.split('\n')
    # start at <div id="main_wrapper"
    for line in search_results:
        if '<a aria-label' in line and 'master' in line:
            link_extension = line.split('href=\"')[1].split('\"')[0]
            break
    # get discogs first result album link
    discogs_album_link = 'https://www.discogs.com' + link_extension

    # get info on the first album link
    album_results = get(discogs_album_link).text.replace('><','>\n<').split('\n')
    # go through the search results and get all the songnames in the album
    for i,line in enumerate(album_results):
        if '<table class=\"tracklist' in line:
            start_index = i
            break
    album_results = album_results[start_index:]
    for i,line in enumerate(album_results):
        if '</table>' in line:
            end_index = i
            break
    tracklist_raw = album_results[:end_index]
    songnames = []
    for line in tracklist_raw:
        if '<span>' in line:
            songname = line.replace('<span>','').replace('</span>','')
            # let's deal with weird html utf-8 numeric references
            songname = html.unescape(songname)
            songnames.append(songname)

    # let's go find the songs on youtube
    # Here's hardcoding the youtube-dl bits
    for i,songname in enumerate(songnames):
        appendable_songname = songname.replace(' ','_')
        appendable_songname = re.sub('[^A-Za-z0-9_]+','',appendable_songname)
        output_filename = os.getcwd() + '/' + appendable_songname + '.mp3'
        YDL_OPTIONS = {
                'format': 'bestaudio',
                'outtmpl':output_filename,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist':'True'
                }
        # now have songlist, album name, and artist name
        query = Artist_Name + ' ' + Album_Name + ' ' + songname
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            ydl.download([video['url']])
        audiofile = eyed3.load(appendable_songname + ".mp3")
        audiofile.tag.title = appendable_songname
        audiofile.tag.artist = Artist_Name
        audiofile.tag.album = Album_Name
        audiofile.tag.album_artist = Artist_Name
        audiofile.tag.track_num = i + 1
        audiofile.tag.save()
    return
    #}}}

if __name__ == '__main__':
    main()
