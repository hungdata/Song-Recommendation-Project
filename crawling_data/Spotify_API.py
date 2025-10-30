
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="b6fdd818bbcb246b5bef8116fc952602",
    client_secret="6d5da08e05a3447abd546b7ab0d72f858",
    redirect_uri="http://127.0.0.1:8080/callback",
    scope="user-library-read"
))

name_song = "Blinding Lights"
# 1. Tìm kiếm bài hát
result = sp.search(q=name_song, type="track", limit=1)
track = result['tracks']['items'][0]

print(" Ngày phát hành:", track['album']['release_date'])
print("Popularity:", track['popularity'])
