from asyncore import write
from spotipy_wrapper import SpotipyWrapper
from myutils import *
from sys import argv
from creds import *
import pprint


""" This script creates a playlist based on a few given artists.
           This can be used for sharing new artists. """

spotify = SpotipyWrapper(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES)
pp = pprint.PrettyPrinter().pprint  # for dev purposes


# parses command line arguments
cl_args = [] if len(argv) == 1 else list(map(int, argv[1:]))
len_arg = len(cl_args)
# no arguments means default values
if len_arg == 0:
    POPULAR_TRACKS = 3         # DEFAULT VALUES
    RANDOM_TRACKS = 3          # DEFAULT VALUES
# 1 argument will use same number for both
elif len_arg == 1:
    POPULAR_TRACKS = RANDOM_TRACKS = cl_args[0]
# 2 arguments will save to popular tracks and random tracks number respectively
elif len_arg == 2:
    POPULAR_TRACKS = cl_args[0]
    RANDOM_TRACKS = cl_args[1]
else:
    print('too many arguments')
    quit()


# 1. get list of artists: through name or link =======

# get artist names/links
artist_names = []
print('          ** NOTE: you might end up with wrong artists **')
print('** if your entry doesn\'t come up first in spotify search results **')
print('\nExact names or links of artists to recommend (enter nothing when finished):')
input_name = input()
while input_name != '':
    artist_names.append(input_name)
    input_name = input()
playlist_name = input('What\'s the playlist name?:\n')

# get artists IDs from names/links provided
pretty_names = []  # stores artist names (pulled from API result instead of user input)
artist_ids = []  # stores artist IDs
for name in artist_names:
    # for artist links
    if name[:8] == 'https://':
        extracted_id = name.split('/')[4].split('?')[0]
        extracted_name = spotify.sp.artist(extracted_id)['name']
    # for artist names
    else:
        artist_result = spotify.search_artist(name, 10)  # gets 10 results
        if artist_result is None:
            print('artist not found: ' + name)
            continue
        extracted_id = artist_result['id']
        extracted_name = artist_result['name']
    artist_ids.append(extracted_id)  # adds artist ID
    pretty_names.append(extracted_name)  # adds artist name

print("\nWorking on the playlist, this might take a while....\n")
# 2. for every artist, grabs 3 most popular and 3 random songs =======

""" dupes can be added in this step if multiple artists share same top tracks.
        TODO: decide to add more tracks if a duplicate was discovered. """

track_ids = []  # stores all tracks returned
# grab tracks from every artist
for a_id in artist_ids:
    track_ids.extend(spotify.artist_top_tracks(a_id, POPULAR_TRACKS))  # grab artist's top 3 tracks
    rand_track = spotify.artist_random_tracks(a_id, amount=RANDOM_TRACKS*2)  # grab random tracks
    # goes through random tracks pulled and only uses non-duplicates
    added = 0
    while added < RANDOM_TRACKS:
        check = rand_track.pop(0)
        if check not in track_ids:
            track_ids.append(check)
            added += 1
track_ids = list(set(track_ids))  # turns to set and back to list to remove duplicates
# TODO: I still need to add code to check for same song dupes but diff IDs

""" # DUPE CHECKING 🛑🛑🛑🛑🛑=============================\
if len(set(track_ids)) < len(track_ids):
    print("🛑🛑🛑🛑🛑STOPPPPP, DUPLICATE🛑🛑🛑🛑🛑")
    print(track_ids)
# DUPE CHECKING 🛑🛑🛑🛑🛑=============================/ """

# 3. create playlist =======
length = len(pretty_names)
# create playlist name if no playlist name was provided
if playlist_name == '':
    playlist_name = 'Songs from ' + (pretty_names[0] if len(pretty_names) == 1 else pretty_names[0] + ' and more')
# constructs playlist description
description = 'Song recommendations from artist'
if length == 1:
    description += f' {pretty_names[0]}.'
elif length == 2:
    description += f's {pretty_names[0]} and {pretty_names[1]}.'
elif length == 3:
    description += f's {pretty_names[0]}, {pretty_names[1]}, and {pretty_names[2]}.'
elif length > 3:
    description += f's {pretty_names[0]}, {pretty_names[1]}, {pretty_names[2]}, and more.'

# creates playlist and returns new playlist ID
new_plist_id = spotify.new_playlist(playlist_name, description=description)
spotify.add_playlist_tracks(new_plist_id, track_ids)
print('\nNew Playlist ID:\n' + new_plist_id)

# 4. Enjoy 😎
