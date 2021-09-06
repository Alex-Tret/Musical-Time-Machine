from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from cred import SPOTIFY_ID, SPOTIFY_SECRET

# import pprint

spotify_scope = "playlist-modify-private"
spotify_redirect = "http://example.com"

music_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = music_date.split("-")[0]

URL = "https://www.billboard.com/charts/hot-100/"

"""Parsing billboard top 100 songs"""
response = requests.get(f"{URL}{music_date}")

web_page = response.text
soup = BeautifulSoup(web_page, "html.parser")
song_names = [name.getText() for name in soup.find_all(name="span",
	class_='chart-element__information__song text--truncate color--primary')]
song_authors = [author.getText() for author in soup.find_all(name="span",
	class_="chart-element__information__artist text--truncate color--secondary")]

"""Authentication with spotify"""
sp = spotipy.Spotify(auth_manager=SpotifyOAuth
(client_id=SPOTIFY_ID,
 client_secret=SPOTIFY_SECRET,
 redirect_uri=spotify_redirect,
 scope=spotify_scope,
 show_dialog=True,
 cache_path="token.txt"))

user_id = sp.current_user()["id"]

"""Spotipy - getting URI's for songs from the Billboard 100"""
song_uris = []
for song in song_names:
	result = sp.search(q=f"track: {song} year: {year}", type="track")
	try:
		uri = result["tracks"]["items"][0]["uri"]
		song_uris.append(uri)

	except IndexError:
		print(f"Song {song} doesn't exists in Spotify. Skipped")



"""Create playlist and add songs URI to it"""
playlist = sp.user_playlist_create(user=user_id, name=f"{music_date} Billboard 100", public="false")

playlist_id = playlist["id"]

add_tracks = sp.playlist_add_items(playlist_id=playlist_id,items=song_uris, position=None)
