import requests
import os
import shutil
from bs4 import BeautifulSoup as bs
import feedparser as rssparser
import yt_dlp
import m3u8
import json
import getpass
import telebot

config = json.loads(open('config.json', 'r').read())

garcom = telebot.TeleBot(config['token'], 'html.parser')
