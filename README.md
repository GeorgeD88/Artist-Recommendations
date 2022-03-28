# Artist Recommendations
This project was a quick 2 hours speed code I did as a fun challenge for myself. What **Artist Recommendations** does is given some artists, it will grab each artist's top 3 songs and 3 random songs, and then creates a playlist out of the pulled songs.<br>
*Unfortunately the screen recording only recorded audio for some reason :,(*

## Running the script
Note before running, you might end up with wrong artists if your entry wouldn't come up first in Spotify search results, so using links instead is favorable.

The file accepts 0 to 2 arguments:
- 0 args: uses default values
- 1 args: uses same value for both number of popular songs and random songs
- 2 args: uses first and second value for each value respectively
```s
$ python3 recommend_artists.py
$ python3 recommend_artists.py 3
$ python3 recommend_artists.py 3 5
```

Once you run it, you will be asked which artists you'd like to be recommended from (through link or name) and then what you'd like to name the playlist. Once it finishes running, you'll have a new playlist<br><br>
**Below is an example run**<br>
<img align="left" src="https://github.com/GeorgeD88/MusicRecommendations/blob/main/artist_recommendations_ex.png" alt="Genre Map" width="45%">
<img align="left" src="https://github.com/GeorgeD88/MusicRecommendations/blob/main/playlist_result.png" alt="Genre Map" width="45%">