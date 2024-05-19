"""Getting data from yaml-file"""
from yaml import load, FullLoader


with open('config.yaml', 'r', encoding='utf-8') as f:
    config = load(f, Loader=FullLoader)

access_token = config['access_token']
