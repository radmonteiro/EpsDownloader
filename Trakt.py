import logging
import json
import time
import datetime
from Auth import Auth
from Requests import Requests
from ConfReader import ConfReader

REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
TRAKT_TOKEN_URL = "https://api.trakt.tv/oauth/token"


class Trakt(object):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    def __init__(self, client_id, client_secret, access_token, user):
        self.req = Requests(client_id, client_secret, access_token, user)
        #self.req.test_collect()

    def get_shows_list(self):
        r = self.req.list()
        logging.debug(r)
        shows = []
        json_obj = json.loads(r)
        for show in json_obj:
            shows.append((show['show']['ids']['trakt'], show['show']['title']))

        for i, s in shows:
            logging.debug( str(i) + ' - ' + s )
        return shows

    def collected_progress(self, show_id):
        content = self.req.collection_progress(show_id)
        logging.debug('------collected------')
        logging.debug(content)
        return json.loads(content)


    def watched_progress(self, show_id):
        content = self.req.watched_progress(show_id)
        logging.debug('----------------')
        logging.debug(content)
        json_show_progress = json.loads(content)

        logging.debug(str(json_show_progress['next_episode']['season']) + ' - ' + str(json_show_progress['next_episode']['number']))
        #next_season = json_eps['next_episode']['season']
        #next_ep = json_eps['next_episode']['number']
        # next_season_size = [x['episodes'] for x in json_show_progress['seasons'] if x['number'] == next_season][0].__len__()
        # print 'next_season_size '+ str(next_season_size)
        return json_show_progress

    @staticmethod
    def next_season_episode(json_show_progress):
        next_season = json_show_progress['next_episode']['season']
        next_ep = json_show_progress['next_episode']['number']
        logging.debug('next_season_episode ' + str(next_season) + " " + str(next_ep))
        return next_season, next_ep

    @staticmethod
    def next_season_size(json_show_progress):
        next_season = json_show_progress['next_episode']['season']
        next_season_size = [x['episodes'] for x in json_show_progress['seasons'] if x['number'] == next_season][
            0].__len__()
        logging.debug('next_season_size ' + str(next_season_size))
        return next_season_size

    @staticmethod
    def list_eps_to_watch(json_show_progress):
        eps_to_watch = []
        next_ep = trakt.next_season_episode(json_show_progress)
        next_season_size = trakt.next_season_size(json_show_progress)
        for i in range(next_ep[1], next_season_size+1):
            logging.debug((next_ep[0], i))
            eps_to_watch.append((next_ep[0], i))
        return eps_to_watch


    def list_eps_to_download(self, show_id, w_pr, c_pr):
        next_to_collect = (c_pr['next_episode']['season'], c_pr['next_episode']['number'])
        next_to_watch = (w_pr['next_episode']['season'], w_pr['next_episode']['number'])
        if next_to_watch[0] > next_to_collect[0] or ( next_to_watch[0] == next_to_collect[0] and next_to_watch[1] > next_to_collect[1]):
            r = self.req.collect(show_id, next_to_watch[0], next_to_watch[1] -1)    #TODO se mudar de season
            logging.debug(r.status_code)
            logging.debug(r.text)

    def my_shows(self, start_date, n_days):
        content = self.req.my_shows(start_date, n_days)
        logging.debug(content)

    def download(self, shows_eps):
        logging.debug(shows_eps)
        #TODO

if __name__ == '__main__':
    conf_reader = ConfReader('Trakt.conf')
    if False: #TODO if token is not valid
        a = Auth()
        t = a.auth(conf_reader.client_id, conf_reader.client_secret)
        conf_reader.write_new_token(t)
    trakt = Trakt(conf_reader.client_id, conf_reader.client_secret, conf_reader.access_token, conf_reader.user)

    trakt.my_shows('2017-02-01', 15)

    exit(0)

    #trakt.auth()
    shows_list = trakt.get_shows_list()
    shows_eps = []
    for show_id, show_name in shows_list:
        w_pr = trakt.watched_progress(show_id)
        #c_pr = trakt.collected_progress(show_id)
        #trakt.next_season_episode(pr)
        eps = trakt.list_eps_to_watch(w_pr)
        for ep in eps:
            print show_name + ' s' + str(ep[0]) + 'ep' + str(ep[1])
        #trakt.list_eps_to_download(show_id, w_pr, c_pr)
        shows_eps.append(ep)


    if conf_reader.last_execution == '':
        trakt.download(shows_eps)
    else:
        date_format = '%Y-%m-%d'
        a = datetime.datetime.strptime(conf_reader.last_execution, date_format)
        a = datetime.strptime(time(date_format), date_format)
        trakt.my_shows(conf_reader.last_execution, )





#os.startfile(magnet_link)


# http://docs.trakt.apiary.io/reference/users/history/get-watched-history
# http://docs.trakt.apiary.io/reference/calendars/my-shows/get-shows

# 1- get list
# 2 - for each show in list http://docs.trakt.apiary.io/reference/shows/watched-progress