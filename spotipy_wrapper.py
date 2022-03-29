from spotipy.oauth2 import SpotifyOAuth
from myutils import *
import spotipy
import random


class SpotipyWrapper:

    GET_MAX = 50
    ADD_MAX = 50
    RANDOM_WILDCARDS = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']

    def __init__(self, client_id, client_secret, redirect_uri, scopes):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scopes
        ))

    def my_id(self) -> str:
        return self.sp.current_user()['id']

    def search_artist(self, search_artist: str, limit: int = 1) -> dict:
        """ Gets first result from artist search query and returns JSON. """
        results = self.sp.search(q='artist:' + search_artist, type='artist', limit=limit)
        try:
            return results['artists']['items'][0]
        except IndexError:
            return None

    def get_artist_link(self, search_artist: str) -> str:
        """ Gets artist link from given search query. """
        return self.search_artist(search_artist)['external_urls']['spotify']

    def artist_albums(self, artist_id: str) -> list:
        """ Returns all albums (IDs) from given artist. """
        results = self.sp.artist_albums(artist_id)
        album_ids = [item['id'] for item in results['items']]
        if results['next']:
            for more_albums in page_results(self.sp, results):
                album_ids.extend(item['id'] for item in more_albums['items'])
        return album_ids

    def artist_tracks(self, artist_id: str) -> list:
        """ Returns all tracks (IDs) from given artist. """
        album_ids = self.artist_albums(artist_id)
        track_ids = []
        for album in album_ids:
                results = self.sp.album_tracks(album)
                for item in results['items']:  # for every song
                    for artist in item['artists']:
                        if artist['id'] == artist_id:  # only adds song if artist is on the track
                            track_ids.append(item['id'])
                if results['next']:
                    for more_tracks in page_results(self.sp, results):
                        for item in more_tracks['items']:  # for every song
                            for artist in item['artists']:
                                if artist['id'] == artist_id:  # only adds song if artist is on the track
                                    track_ids.append(item['id'])
        return track_ids

    def artist_random_tracks(self, artist_id: str, amount: int = 1) -> str:
        """ Returns random track from given artist. """
        artist_tracks = self.artist_tracks(artist_id)  # VERY TAXING MOVE
        random_tracks = []
        for a in range(amount):
            i = random.randrange(len(artist_tracks)) # get random index
            artist_tracks[i], artist_tracks[-1] = artist_tracks[-1], artist_tracks[i]    # swap with the last element
            random_tracks.append(artist_tracks.pop())
        return random_tracks

    def artist_top_tracks(self, artist_id: str, amount: int = None) -> list:
        """ Returns given artist's top tracks. """
        results = self.sp.artist_top_tracks(artist_id)['tracks']
        if len(results) < amount:
            amount = len(results)
        top_tracks = []
        for track in results[:amount]:
            top_tracks.append(track['id'])
        return top_tracks

    def get_playlist_tracks(self, playlist_id: str):
        """ Returns all tracks (IDs) in given playlist. """
        results = self.sp.playlist_tracks(playlist_id)
        plist_tracks = [item['track']['id'] for item in results['items']]
        if results['next']:
            for more_albums in page_results(self.sp, results):
                plist_tracks.extend(item['track']['id'] for item in more_albums['items'])
        return plist_tracks

    def new_playlist(self, playlist_name: str, public: bool = True, collaborative: bool = False, description: str = None):
        """ Creates new playlist with given name and returns playlist ID. """
        return self.sp.user_playlist_create(self.my_id(), playlist_name, public=True, collaborative=False, description=description)['id']

    def add_playlist_tracks(self, playlist_id: str, tracks: list):
        """ Adds list of tracks to given playlist. """
        tracks_chunks = divide_chunks(tracks, self.ADD_MAX)
        for chunk in tracks_chunks:
            self.sp.playlist_add_items(playlist_id, chunk)

    # # SEARCH BASED (w/ wildcards)
    # def artist_random_tracks(self, artist_id: str, amount: int = 1) -> str:
    #     """ Returns random track from given artist. """
    #     wildcard = random.choice(self.RANDOM_WILDCARDS)
    #     results = self.sp.search(q=f'artist:{artist_id} track:{wildcard}', type='track', limit=amount)
    #     """
    #     track_ids = []
    #     for track in results['tracks']:
    #         track_ids.append(track['id'])
    #     """
    #     return results

    # FAIL
    ''' def search_artist(self, search_artist: str, limit: int = 1) -> dict:
        """ Gets results from artist search query and returns JSON. """
        search_artist = search_artist.lower()
        results = self.sp.search(q='artist:' + search_artist, type='artist', limit=limit)
        r_items = results['artists']['items']
        if len(r_items) == 0:  # short circuits if no results
            return None
        else:
            r_item = r_items[0]
            a_name = r_item['name'].lower()
        while a_name != search_artist:
            print(a_name)
            # if results exist, checks to page
            if results['artists']['next'] is not None:
                results = self.sp.next(results['artists'])
                if len(results['artists']['items']) == 0:  # short circuits if no results
                    return None
                r_item = results['artists']['items'][0]
                a_name = r_item['name'].lower()
            else:
                break
        return r_item '''