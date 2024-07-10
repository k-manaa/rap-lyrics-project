import time
import pandas as pd
import requests
import lyricsgenius  # from https://github.com/johnwmillr/LyricsGenius
from typing import List, Dict, Any

def search_songs_by_artist(artist_name: str, retries: int = 7, delay: int = 10, start_index: int = 0) -> Tuple[List[Dict[str, Any]], int]:
    """Searches for songs by the given artist and returns song metadata.

    Args:
        artist_name (str): The name of the artist.
        retries (int): The number of times to retry fetching songs in case of failure (default: 7).
        delay (int): The delay in seconds between retries (default: 10).
        start_index (int): The index of the first song to start fetching (default: 0).

    Returns:
        Tuple[List[Dict[str, Any]], int]: A tuple containing a list of song metadata and the index of the last processed song.
    """
    artist_object = None
    for _ in range(retries):
        try:
            artist_object = genius.search_artist(artist_name, max_songs=100)
            if start_index >= len(artist_object.songs):
                return [], start_index
            break
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for artist {artist_name}. Retrying...")
            time.sleep(delay)
            continue
        except Exception as e:
            print(f"Failed to fetch songs for artist {artist_name}: {e}")
            return [], start_index
    if artist_object is None:
        print(f"Failed to fetch songs for artist {artist_name} after {retries} attempts")
        return [], start_index

    song_metadata = []
    for i, song in enumerate(artist_object.songs[start_index:]):
        try:
            song_url = genius_base_url + '/songs/' + str(song.id)
            response = requests.get(song_url, headers=headers)
            song_data = response.json()['response']['song']

            release_date = song_data.get('release_date')
            if release_date is None:
                release_date = 'Unknown'

            lyrics = song.lyrics
            if lyrics:
                # clean up the lyrics
                lyrics = lyrics.split('\n')
                lyrics = [line for line in lyrics if not line.startswith('[')]
                lyrics = ' '.join(lyrics)
            else:
                lyrics = "Cannot find the lyrics"

            song_meta = {
                'release_date': release_date,
                'artist_name': artist_name,
                'title': song.title,
                'lyrics': lyrics
            }
            song_metadata.append(song_meta)
        except requests.exceptions.Timeout:
            print(f"Timeout occurred while processing song {song.title} by artist {artist_name}. Skipping this song.")
            return song_metadata, i + start_index
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while processing song {song.title} by artist {artist_name}: {e}")
            continue

    return song_metadata, len(artist_object.songs)


def save_lyrics_to_csv(artist_names: List[str], file_name: str) -> None:
    """Saves the lyrics of songs by the given artists to a CSV file.

    Args:
        artist_names (List[str]): A list of artist names.
        file_name (str): The name of the output CSV file.
    """
    lyrics_list = []
    last_processed_index = {artist: 0 for artist in artist_names}
    for i, artist_name in enumerate(artist_names):
        while True:
            try:
                print(f'Fetching songs for artist {artist_name}')
                song_metadata, last_processed_index[artist_name] = search_songs_by_artist(artist_name, start_index=last_processed_index[artist_name])
                if not song_metadata:
                    print(f'No more songs found for artist {artist_name}')
                    break
                lyrics_list.extend(song_metadata)
                if last_processed_index[artist_name] >= 101:
                    break 
            except Exception as e:
                print(f"Failed to fetch songs for artist {artist_name}: {e}")
                continue

            # Add data to .csv after every artist or at the end of the list
            if (i + 1) % 1 == 0: #or i == len(artist_names) - 1:
                df = pd.DataFrame(lyrics_list)
                if i == 0:
                    # change header for the first entry
                    df.to_csv(file_name, index=False)
                else:
                    # don't change header for subsequent entries
                    df.to_csv(file_name, mode='a', header=False, index=False)

                # empty list for new batch    
                lyrics_list = [] 
                time.sleep(30) # wait time in seconds, to avoid API rate limit


def main() -> None:
    """Main function that scrapes lyrics for a given artist and saves them to a CSV file."""
    rapper_names = ['Tupac']
                    # ['Jay-Z', 'Nas', 'Eminem', 'The Notorious B.I.G.', 'Lil Wayne', 'Kanye West', 'Method Man', 'Dr.Dre']

    save_lyrics_to_csv(rapper_names, 'lyrics_rapper_name.csv')


if __name__ == '__main__':
    main()
