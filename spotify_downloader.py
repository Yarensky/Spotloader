from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl

def get_spotify_tracks(playlist_url, client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = Spotify(auth_manager=auth_manager)

    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    
    tracks = []
    offset = 0
    limit = 100  # Spotify API max limit

    while True:
        results = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        items = results['items']

        for item in items:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            tracks.append(f"{track_name} {artist_name}")

        if len(items) < limit:
            # No more items to fetch
            break

        offset += limit

    return tracks

def download_from_youtube(track_name, download_path):
    try:
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
                'quiet': True,
                'no_warnings': True,
                'retries': 3,
                'continuedl': True
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return f"Downloading finished: {track_name}"
        else:
            return f"Video not found for: {track_name}"
    except Exception as e:
        return f"An error occurred: {str(e)}. Skipping to next track."

def download_playlist(playlist_url, download_path, client_id, client_secret):
    tracks = get_spotify_tracks(playlist_url, client_id, client_secret)
    total_tracks = len(tracks)

    with ThreadPoolExecutor(max_workers=2) as executor:  # Use 2 threads
        futures = {executor.submit(download_from_youtube, track_name, download_path): track_name for track_name in tracks}

        for index, future in enumerate(as_completed(futures), start=1):
            track_name = futures[future]
            result = future.result()
            print(f"[{index}/{total_tracks}] {result}")

def main():
    while True:
        playlist_url = input("Paste spotify playlist link: ")
        download_path = input("Paste directory path: ")

        # Add your Spotify Dev credentials
        client_id = 'clientID'
        client_secret = 'ClientSecret'

        download_playlist(playlist_url, download_path, client_id, client_secret)

        print("\n" + "-"*40)
        print("Menu:")
        print("Press 1 to download another playlist")
        print("Press 2 to exit")
        
        choice = input("Enter your choice: ")
        if choice == '2':
            break

if __name__ == "__main__":
    main()
