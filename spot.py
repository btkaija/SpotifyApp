import sys, time
import requests
import spotipy
import spotipy.util as util
import pprint
import m3u_lexer

def GetAlbumDate(sp, album_id):
    album_info = sp.album(album_id)
    date = album_info['release_date']
    precision = album_info['release_date_precision']
    print (date, precision)
    return album_info['release_date']

def PromptUserForSong(result_list):
    if (len(result_list)):
        isGoodInput = False
    else:
        print("No results were found.")
        isGoodInput = True

    while(not isGoodInput):
        try:
            in_val = int(input("\nEnter the song # that matches the search best. --> "))
            if(in_val >= 0 and in_val < len(result_list)):
                isGoodInput = True
            else:
                print ("The value entered", in_val, "is not a valid song number.")
        except:
            print("Invalid integer input.")
    return in_val

def init_spotify_connection():
    print("Attempting login to spotify API.")
    client_id = "ba9fba82b5eb41e39530e6f3095cba4b"
    client_secret = "699b0be3fa2c424295db30cbd26dedc8"
    my_callback = r"http://localhost/"
    scope = '''user-library-read user-library-modify
               user-follow-read playlist-modify-private
               playlist-modify-public playlist-read-private'''

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Please enter username as first argument.")
        sys.exit()
    return util.prompt_for_user_token(username, scope, client_id, client_secret, my_callback)


##begin main function

print("Parsing the playlist for songs")

songs = m3u_lexer.read_m3u_playlist('Best.m3u', False)
song_path = [song.split(" XXX ")[1] for song in songs]
song_names = [song.split(" XXX ")[0].split('-')[1] for song in songs]
song_artists = [song.split(" XXX ")[0].split('-')[0] for song in songs]

token = init_spotify_connection()

if token:
    print("Successful login to spotify API.")
    sp = spotipy.Spotify(auth=token)
    print("Searching for",songs[0], '\n')
    results = sp.search(song_names[0] +  " " + song_artists[0])
    result_list = results['tracks']['items']
    for i in range(0, len(result_list)) :
        song_name = result_list[i]['name']
        song_artists = [artist['name'] for artist in result_list[i]['artists']]
        song_id = result_list[i]['id']
        song_album = result_list[i]['album']
        #song_album_date = GetAlbumDate(sp, song_album['id'])
        song_album_name = song_album['name']
        print("Song #"+str(i)+" found -->", song_name, '-',
            song_artists, '-', song_album_name)

    index_selected = PromptUserForSong(result_list)
    print("selected song number", index_selected, "with id", song_id)

else:
    print("Can't get token for", username)
