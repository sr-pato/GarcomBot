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
import urllib.parse as urlparse 
import re


config = json.loads(open('config.json', 'r').read())

garcom = telebot.TeleBot(config['token'], 'html.parser')

def write_error(error: str):
    pass



def link_of(link: str) -> str or None:
    """Verifica se o link dado está entre as plataformas aceitas, caso não, retorna 'None'"""
    link = urlparse.urlsplit(link)
    for plataforma in config['plataformas']:
        if link.path in config['plataformas'][plataforma] or link.netloc in config['plataformas'][plataforma]:
            return plataforma
    return None
    

def down_ifunny(link: str) -> str:
    """Retorna link direto de vídeo em embed do ifunny"""
    session = requests.Session()
    session.headers['user-agent'] = config['user-agent']['linux']
    page = bs(requests.get(link).content, 'html.parser')
    try:
        direct_link = page.find('video')['data-src']
    except:
        write_error(config['msg_erros']['video_not_found_ifunny'])
    else:
        session.close()
        return direct_link


def down_for_direct_link(link: str, filename: str, path: str):
    session = requests.Session()
    session.headers['user-agent'] = config['user-agent']['linux']
    
