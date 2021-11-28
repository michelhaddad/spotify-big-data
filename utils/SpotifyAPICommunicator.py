import pandas as pd
import spotipy
from spotipy import SpotifyClientCredentials


class SpotifyAPICommunicator:
    def __init__(self, client_id, client_secret):
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def fetch_audio_features(self, track_ids: []):
        fields = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability',
                  'key', 'duration_ms', 'loudness', 'mode', 'valence']
        features = pd.DataFrame(columns=['track_id'] + fields)

        for track_id in track_ids:
            audio_features = self.sp.audio_features(track_id)
            if audio_features[0] is None:
                pass
            else:
                row = [track_id] + [audio_features[0][k] for k in fields]
                features = features.append(pd.Series(data=row, index=features.columns.values), ignore_index=True)

        features['mode'] = features['mode'].astype(int)
        features['key'] = features['key'].astype(int)
        return features

    def fetch_artists_info(self, artist_names: []):
        artist_info = pd.DataFrame()

        for name in artist_names:
            results = self.sp.search(q='artist:' + name, type='artist')
            # assume first search result is the artist we want
            if results['artists']['items'][0]['name'] == name:
                tmp = {'artist': results['artists']['items'][0]['name'],
                       'genres': results['artists']['items'][0]['genres'],
                       'popularity': results['artists']['items'][0]['popularity'],
                       'followers': results['artists']['items'][0]['followers']['total'],
                       'artist_id': results['artists']['items'][0]['uri'][-22:]}

                artist_info = artist_info.append(tmp, ignore_index=True)

        artist_info['followers'] = artist_info['followers'].astype(int)
        artist_info['popularity'] = artist_info['popularity'].astype(int)
        return artist_info
