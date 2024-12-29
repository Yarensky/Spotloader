# Spotloader
Enhanced Spotify downloader script

1. First things first. Perform these steps before using the script. These are mandatory libraries to run Spotloader

- Open shell as administrator and type:  
   ```
   pip install spotipy youtube-search-python yt-dlp
   

- Get your ClientID and ClientSecret by logging into developer.spotify.com
  Go to the dashboard (https://developer.spotify.com/dashboard)
  Create app (app name/description/redirectURIs are irrevelant)

  Paste ClientID in line 86 in .py code

  Paste ClientSecret in line 87 in .py code
   
- Download ffmpeg from https://www.gyan.dev/ffmpeg/builds/
  
  Extract all files to any folder (for example C:\FFMPEG) and add it's bin folder (C:\ffmpeg\bin) to both PATH variables in environmental variables settings.
  
  Restart your computer after adding the variables

- Install Get cookies.txt locally (https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
  
  This prevents script errors if some tracks has age restrictions
  
  Log in into youtube, click on add-in, Export As.. and save .txt file as ytcookies.txt (this filename has been set in code)


2. Now when you're all set. Create a folder and paste all three files: spotify_downloader.py, run_downloader.bat and ytcookies.txt into it.

3. Run .bat file and wait till it starts.
4. Paste your spotify link (REMEMBER: playlist cannot have any emoji or other similar symbols in name)
5. Paste directory path where you want to save the mp3's 
