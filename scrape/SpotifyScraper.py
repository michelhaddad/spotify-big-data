from datetime import date, timedelta
import requests
from io import BytesIO
import pandas as pd
from pandas.errors import ParserError


class SpotifyScraper:
    SPOTIFY_TOP_200_GLOBAL_URL = 'https://spotifycharts.com/regional/global/daily/%s/download'

    def __fetch_top_200_chart(self, date: date, request_headers: dict, request_cookies: dict):
        url = self.SPOTIFY_TOP_200_GLOBAL_URL % date.strftime('%Y-%m-%d')
        response = requests.get(url, headers=request_headers, cookies=request_cookies)
        if response.status_code == 200:
            encodedObject = BytesIO(response.text.encode('utf8', 'ignore'))
            try:
                df = pd.read_csv(encodedObject, header=1)
            except ParserError:
                print('Invalid format error. url: %s' % url)
                return None

            df['date'] = date
            df['region'] = 'Global'
            df['track_id'] = df['URL'].str[-22:]

        else:
            raise Exception('An error occured:\nResponse status code: %d\nError Message : %s' % (
                response.status_code, response.reason))

        return df

    def get_top_200_charts_in_range(self, start_date: date, end_date: date, request_headers: dict,
                                    request_cookies: dict):
        streams = pd.DataFrame()

        while start_date < end_date:
            df = self.__fetch_top_200_chart(start_date, request_headers, request_cookies)
            if df is not None:
                streams = streams.append(df)
            start_date += timedelta(1)

        return streams
