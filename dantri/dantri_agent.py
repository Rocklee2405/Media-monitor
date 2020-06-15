import requests
import re
import os
import json
import logging
import wget

url = "https://dantri.com.vn/"
ids_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ids_handled.txt')
data_temp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

headers = {
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}


def get_current_ids():

    response = requests.request("GET", url, headers=headers, timeout=10)
    matches = re.finditer(r'(\d{17}).htm', response.text, re.MULTILINE)
    id_set = set()
    if os.path.exists(ids_file):
        with open(ids_file) as file_data:
            id_set_handled = file_data.read().split('\n')
    else:
        id_set_handled = []
    for matchNum, match in enumerate(matches, start=1):
        id_set.add(match.group(1))

    id_need_handle = id_set - set(id_set_handled)

    save_ids_handled = (list(id_need_handle) + id_set_handled)[:10000]
    with open(ids_file, 'w') as file_data:
        for item_id in save_ids_handled:
            file_data.write("{}\n".format(item_id))
    return id_need_handle


def handle_ids(id_paper):
    try:
        data_info = requests.get('https://webapi.dantri.com.vn/audio-info/{}'.format(id_paper)).json()
        title_audio = data_info['source']['TitleAudio'][0]['Value']
        sapo_audio = json.loads(data_info['source']['SapoAudio'])[0]['Value']
        body_audio = data_info['source']['BodyAudio'][0]['Value']
        return "https://acdn.dantri.com.vn/??{},{},{}".format(title_audio, sapo_audio, body_audio)
    except:
        logging.error("Error access audio {}".format(id_paper))
        return None


def get_current_audio_file():

    if not os.path.exists(data_temp):
        oldmask = os.umask(000)
        os.makedirs(data_temp,  mode=0o777, exist_ok=False)
        os.umask(oldmask)
    id_need_handle = get_current_ids()
    for id_paper in id_need_handle:
        audio_url = handle_ids(id_paper)
        if audio_url:
            download_file_path = os.path.join(data_temp, "{}.mp3".format(id_paper))
            wget.download(audio_url, download_file_path)
            if os.path.exists(download_file_path) and os.path.getsize(download_file_path) > 100:
                logging.info("Downloaded {} bytes in file {}".format(os.path.getsize(download_file_path), audio_url))
                yield download_file_path
