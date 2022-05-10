import requests
import rfid_read
import spotipy
import spotipy.util as util
import rfid_write
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
from dateutil import parser

#Spotify API authentication
scope = "streaming user-read-playback-state user-modify-playback-state playlist-modify-public playlist-read-collaborative playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='509c26730d4f47aeac7850e506e3c222', client_secret='52474036b2624aa780d483417666a117', redirect_uri='http://localhost:8080/callback', scope=scope))
token = util.prompt_for_user_token('JakieWakey', scope, client_id='509c26730d4f47aeac7850e506e3c222', client_secret='52474036b2624aa780d483417666a117', redirect_uri='http://localhost:8080/callback')

#initializing variables
current_albums = dict()
temp_albums = dict()
playlist_id = '6gLVrKiDjScagRNviW2vCL'

#raspotify connection
selfDevice = ''
for device in sp.devices()['devices']:
    if str(device['name']) == 'Beat Box':
        selfDevice = str(device['id'])
        print('device initiated: ' + selfDevice)
if selfDevice == '':
    print('raspotify not running')

#main loop
while True:
    #loop through current_albums and delete album if its stale (5 sec)
    for album, time in current_albums.items():
        if time < datetime.datetime.now():
            print(str(sp.album(album)['name']) + ' has expired')
            tracks = sp.album_tracks(album)
            tracklist = []
            for track in tracks['items']:
                tracklist.append(track['uri'])
            sp.playlist_remove_all_occurrences_of_items(playlist_id, tracklist)
            print('deleting')
        else:
            temp_albums[album] = time
    if temp_albums != current_albums and not temp_albums:
        try:
            sp.pause_playback(device_id=selfDevice)
        except:
            print('device not found for pause')
    else:
        if temp_albums != current_albums:
            try:
                sp.start_playback(device_id=selfDevice, context_uri='spotify:playlist:'+playlist_id)
                sp.shuffle(True, device_id=selfDevice)
            except:
                print('device not found')
    current_albums = temp_albums
    temp_albums = {}
    
    #read rfid and check if its new
    albumID = rfid_read.read()
    if albumID is not None:
        albumID = str(albumID.strip())
        inAlbumList = False
        for album in current_albums:
            if albumID == album:
                inAlbumList = True
        #if the album is new, give it a stale time and add the tracks to the playlist        
        if inAlbumList == False:
            try:
                print(str(sp.album(albumID)['name']))
                tracks = sp.album_tracks(albumID)
                print("adding")
                current_albums[albumID] = datetime.datetime.now()+datetime.timedelta(0,1)
                tracklist = []
                for track in tracks['items']:
                    tracklist.append(track['uri'])
                sp.playlist_add_items(playlist_id, tracklist)
                sp.start_playback(device_id=selfDevice, context_uri='spotify:playlist:'+playlist_id)
                sp.shuffle(True, device_id=selfDevice)
            except:
                print("misread tag")
                
            
        #if the album is old, refresh the stale time
        else:
            inAlbumList = False
            current_albums[albumID] = datetime.datetime.now()+datetime.timedelta(0,1)