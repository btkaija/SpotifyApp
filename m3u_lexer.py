import sys
from os import listdir

path = "Playlists/"

def ctor():
    if len(sys.argv) > 2:
        playlist_name = sys.argv[1]
        print_songs = sys.argv[2] == 'True'
    else:
        print("Please enter playlist name as first argument.")
        print("Please enter boolean (True or False) as second argument.")
        sys.exit()


def read_m3u_playlist(playlist_name, print_songs):
    f = open (playlist_name, encoding = 'UTF8', errors='ignore')

    songs = []
    for line in f:
        #print("line -->  ", line)
        if (line.find('#EXTINF') != -1):
            file_name = line.split(',')[1].strip()
            file_path = f.readline().strip()
            songs.append( file_name + " XXX " + file_path)

            print(file_path)

    print ('Found ', len(songs) , 'songs in the playlist ', playlist_name)
    if (print_songs):
        for song in songs:
            print(song)
    else:
        print ('Not printing all song names found.')
    return songs

def get_playlist_names(directory):
    return listdir(directory)

# playlist_names =  get_playlist_names(path)
# for name in playlist_names:
#     read_m3u_playlist(path+name, False)
