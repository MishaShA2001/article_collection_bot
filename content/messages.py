"""Unpack bot messages from yaml-file"""
from yaml import load, FullLoader


with open('content/messages.yaml', 'r', encoding='utf-8') as f:
    messages = load(f, Loader=FullLoader)
