import requests


class Requests:
    def __init__(self, client_id, client_secret, access_token, user):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.user = user

    def get_auth_headers(self):
        return {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + self.access_token,
                   'trakt-api-version': 2,
                   'trakt-api-key': self.client_id
                   }

    def my_shows(self, start_date, n_days):
        r = requests.get('https://api.trakt.tv/calendars/my/shows/' + start_date + '/' + str(n_days),
                         headers=self.get_auth_headers())
        return r.content

    def my_progress(self):
        r = requests.get('https://api.trakt.tv/shows/id/progress/watched?hidden=false&specials=false&count_specials=true')

    def list(self):
        headers = {'Content-Type': 'application/json',
                   'trakt-api-version': 2,
                   'trakt-api-key': self.client_id
                   }
        r = requests.get('https://api.trakt.tv/users/'+self.user+'/lists/towatch/items/shows', headers=headers)
        return r.content

    def watched_progress(self, show_id):
        return requests.get('https://api.trakt.tv/shows/' + str(
            show_id) + '/progress/watched?hidden=false&specials=false&count_specials=true',
                         headers=self.get_auth_headers()).content

    def collection_progress(self, show_id):
        return requests.get('https://api.trakt.tv/shows/' + str(
            show_id) + '/progress/collection?hidden=false&specials=false&count_specials=false',
                     headers=self.get_auth_headers()).content

    def collect(self, show_id, season, ep):
        body = {
            'shows': [
                {
                    'ids':{
                        'trakt': show_id
                    },
                    'seasons':[
                        {
                            'number': season,
                            'episodes': [
                                {
                                    'number': ep
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        return requests.post('https://api.trakt.tv/sync/collection', headers=self.get_auth_headers(), data=body)

    def test_collect(self):
        body = {
            "movies": [],
            "shows": [],
            "episodes": [
                {
                    "ids": {
                      "trakt": 2052057,
                      "tvdb": 5398852,
                      "imdb": "tt5143508",
                      "tmdb": 1136314,
                      "tvrage": 0
                    }
                }
            ]
        }
        return requests.post('https://api.trakt.tv/sync/collection', headers=self.get_auth_headers(), data=body)
