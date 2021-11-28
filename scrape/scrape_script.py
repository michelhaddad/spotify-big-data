import pandas as pd
from datetime import date
from scrape.SpotifyScraper import SpotifyScraper
from utils.SpotifyAPICommunicator import SpotifyAPICommunicator

client_id = 'client_id'
client_secret = 'client secret'
spotify_scraper = SpotifyScraper(client_id, client_secret)
spotify_api_communicator = SpotifyAPICommunicator(client_id, client_secret)

start_date = date(2019, 1, 1)
end_date = date(2020, 1, 1)
date_string = start_date.strftime('%Y-%m-%d') + '__' + end_date.strftime('%Y-%m-%d')
headers = {}
cookies = {}

print('Gathering top 200 charts ...')
top_200_charts_data = spotify_scraper.get_top_200_charts_in_range(start_date, end_date, headers, cookies)
top_200_charts_data.to_csv('../data/streams_%s.csv' % date_string, index=False)
print('Saved top 200 charts !')

streams = pd.read_csv('../data/streams_%s.csv' % date_string)

print('Fetching song features ...')
track_ids = streams['track_id'].unique()
features = spotify_api_communicator.fetch_audio_features(track_ids)
features.to_csv('../data/song_features_%s.csv' % date_string, index=False)
print('Saved song features!')

print('Gathering artist information ...')
artist_names = streams['Artist'].unique()
artist_names = artist_names[~pd.isnull(artist_names)]
artist_info = spotify_api_communicator.fetch_artists_info(artist_names)
artist_info.to_csv('../data/artist_info_%s.csv' % date_string, index=False)
print('Saved artist information')
