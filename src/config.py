import json
import yaml


class Config():
    CLIENT_ID = json.loads(
        open('client_secrets.json', 'r').read())['web']['client_id']

    with open("params.yaml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    @staticmethod
    def get_client_id():
        return Config.CLIENT_ID

    @staticmethod
    def get_cfg():
        return Config.cfg
