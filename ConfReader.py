import json


class ConfReader:
    def __init__(self, file_name):
        with open(file_name) as data_file:
            data = json.load(data_file)
        self.last_execution = data['last_execution']
        self.access_token = data['access_token']
        self.user = data['user']
        self.client_id = data['client_id']
        self.client_secret = data['client_secret']
        self.last_exec = data['last_exec']

    def last_execution(self):
        return self.last_execution

    def access_token(self):
        return self.access_token

    def user(self):
        return self.user

    def client_id(self):
        return self.client_id

    def client_secret(self):
        return self.client_secret

    def last_exec(self):
        return self.last_exec

    def write_new_token(self, token):
        # TODO
        return ''
