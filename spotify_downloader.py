import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl

def get_spotify_tracks(playlist_url, client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = Spotify(auth_manager=auth_manager)

    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    
    tracks = []
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        tracks.append(f"{track_name} {artist_name}")
    
    return tracks

def download_from_youtube(track_name, download_path):
    search = VideosSearch(track_name, limit=1)
    search_results = search.result()
    if search_results['result']:
        video_info = search_results['result'][0]
        video_url = video_info['link']
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookies': os.path.join(os.path.dirname(__file__), "ytcookies.txt"),
            'quiet': True,  # Quiet mode to remove unnecessary alerts
            'no_warnings': True,  # shut off alerts
            'retries': 3,  # Number of retries of download attempts
            'continuedl': True  # Continue downloading by skipping error
        }
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    else:
        print(f"Video not found for: {track_name}")

def main():
    playlist_url = input("Paste spotify playlist link: ")
    download_path = input("Paste directory path: ")

    # Add Your Spotify Dev credentials
    client_id = 'ClientIDinSingleQuotes'
    client_secret = 'ClientSecretInSingleQuotes'

    tracks = get_spotify_tracks(playlist_url, client_id, client_secret)
    for track_name in tracks:
        print(f"Downloading: {track_name}")
        try:
            download_from_youtube(track_name, download_path)
        except Exception as e:
            print(f"An download error ocurred: {track_name}. Skipping to next track.")
            continue
        print(f"Downloading finished: {track_name}")

if __name__ == "__main__":
    main()