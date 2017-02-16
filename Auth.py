import requests
import json

from oauthlib.oauth1.rfc5849.endpoints import access_token


class Auth(object):
    @staticmethod
    def auth(client_id, client_secret):
        url = 'https://trakt.tv/oauth/authorize?response_type=code&client_id=' + client_id + '&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
        print url

        headers = {'Content-Type' : 'application/json'}
        payload = {'client_id' : client_id}
        r = requests.post('https://api.trakt.tv/oauth/device/code', headers = headers, data = json.dumps(payload))

        data = json.loads(r.text)
        code = data['device_code']
        verification_url = data['verification_url']
        user_code = data['user_code']

        print 'Copy the code ' + user_code + ', go to ' + verification_url + ' and enter this code.'
        raw_input('Then, press Enter to continue...')

        payload = {'code': code,
                   'client_id': client_id,
                   'client_secret': client_secret
                   }
        r = requests.post('https://api.trakt.tv/oauth/device/token', headers = headers, data = json.dumps(payload))
        data = json.loads(r.text)
        token = data['access_token']
        print token

        return token

        #r1 = conn.getresponse()
        #print r1.status, r1.reason