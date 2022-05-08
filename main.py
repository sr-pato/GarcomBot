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
import time


config = json.loads(open('config.json', 'r').read())

garcom = telebot.TeleBot(config['token'], 'HTML')

def create_session(user_agent):
    "Retorna uma sessão novinha em folha"
    session = requests.Session()
    session.headers['user-agent'] = user_agent
    return session


def write_error(error: str):
    pass


def create_folder(path: str):
    "Cria pasta caso ela não exista"
    if not os.path.exists(path):
        os.mkdir(path)


def clear(dest):
    "Isso daqui é só pra remover arquivos temporários"
    os.remove(dest)


def send_file(dest, msg, extension):
    "Envia arquivo para a conversa dependendo da sua extensão"
    if extension in config['extensions']['video']:
        garcom.send_video(msg.chat.id, open(dest, 'rb').read(), supports_streaming=True)

    
def link_of(link: str):
    """Verifica se o link dado está entre as plataformas aceitas, caso não, retorna 'None'"""
    link = urlparse.urlsplit(link)
    for plataforma in config['plataformas']:
        if link.path in config['plataformas'][plataforma] or link.netloc in config['plataformas'][plataforma]:
            return plataforma


def down_ifunny(link: str) -> str:
    """Retorna link direto de vídeo em embed do ifunny"""
    session = create_session(config['user-agent']['linux'])
    page = bs(session.get(link).content, 'html.parser')
    try:
        direct_link = page.find('video')['data-src']
    except:
        write_error(config['msg_erros']['video_not_found_ifunny'])
    else:
        session.close()
        return direct_link
        

def down_for_direct_link(link: str, filename: str, path: str):
    "Faz download do link argumentado salva na pasta com o filename inserido!"
    session = create_session(config['user-agent']['linux'])
    if not os.path.exists(path):
        with open(path+filename, 'wb') as fileDonw:
            response = session.get(link, stream=True)
            for chunk in response.iter_content(1024**2):
                fileDonw.write(chunk)
    else:
        write_error(config['msg_erros']['file_exists'])
    session.close()
    return None


def down_for_direct_link_progress(link: str, filename: str, path: str, msg):
    "Faz download do link com barra de progresso no telegram salva na pasta com o filename inserido!"
    session = create_session(config['user-agent']['linux'])
    with open(path+filename, 'wb') as fileDonw:
        response = session.get(link, stream=True)
        baixado = size = int(response.headers['content-length'])
        for chunk in response.iter_content(10240):
            baixado -= 10240
            fileDonw.write(chunk)
            garcom.edit_message_text(f"<b>BAIXANDO!!!</b>\n\nArquivo: <code>{filename}</code>\nTotal: <code>{round(size)} Bytes</code>\nBaixado: <code>{round(baixado)} Bytes</code>\nProgresso: <code>{round(100-(baixado*100)/size)}%</code>", msg.chat.id, msg.message_id)
            clear(path+filename)
        fileDonw.close()
    session.close()
    return None


def direct_link_tiktok(link):
    session = create_session(config['user-agent']['linux'])
    page = bs(session.get(link).content, 'html.parser')
    



def get_file_extension(filename_or_path: str) -> str:
    "Retorna a extensão de algum arquivo"
    extension = filename_or_path.split('.')[-1]
    return extension


### Commands
@garcom.message_handler(['downn'])
def verify(msg):
    message = garcom.reply_to(msg, 'Blz, to vendo isso aí...')
    links = msg.text.split(' ')[1:]
    for link in links:
        plataforma = link_of(link)
        if not plataforma == None:
            if plataforma == 'ifunny':
                direct_link = down_ifunny(link)
                extension = get_file_extension('ifunny.mp4')
                create_folder(config['paths']['temps'])
                down_for_direct_link_progress(direct_link, 'ifuuny.mp4', config['paths']['temps'], message)
                time.sleep(0.1)
                send_file(config['paths']['temps']+'/ifuuny.mp4', message, extension)                
                garcom.delete_message(msg.chat.id, message.message_id)
            elif:
                plataforma == 'tiktok':


    

garcom.polling(non_stop=True)
