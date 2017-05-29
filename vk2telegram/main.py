# -*- coding: UTF-8 -*-
import datetime
import logging
import os
import pprint
import sys
import time
import urllib

import io
import numpy as np
import requests
import telegram
import vk
from PIL import Image
import shutil

logger = logging.getLogger('vk')
logger.setLevel(logging.DEBUG)
APP_ID = 000000
CHANNEL = 'Розваги'
CHAT_ID = '@memesFromKvis'
BOT_TOKEN = '00000000000000000000'

IGNORE_EXT = ['srt', 'doc']

bot = telegram.Bot(BOT_TOKEN)

if not os.path.isfile('access_token.txt'):
    access_token = ''
else:
    access_token = ''
    with open('access_token.txt') as f:
        access_token = f.read()

if access_token == '':
    print('No access token.')
    print(
        'Open https://oauth.vk.com/authorize?client_id={id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=video,friends,wall,offline&response_type=token'.format(
            id=APP_ID))

    sys.exit(0)

if not os.path.isdir('mem'):
    os.mkdir('mem')

session = vk.Session(access_token=access_token)
api = vk.API(session)
lists = list(api.newsfeed.getLists())

print('lists', lists[:])

c_id = 0

for l in lists[1:]:

    if l['title'] == CHANNEL:
        c_id = l['id']

if not c_id:
    print('No channel')
    sys.exit(0)

news = api.newsfeed.get(source_ids="list{}".format(c_id), count=100, startfrom=time.time() - 1800, filters='post')


def upload_doc(f, caption, filename='file.gif'):
    r = requests.post("https://api.telegram.org/bot{token}/sendDocument?{str_params}".format(
        token=BOT_TOKEN, str_params=urllib.parse.urlencode({
            'caption': caption,
            'chat_id': CHAT_ID,
            'parse_mode': 'HTML'
        })
    ), files={'document': (filename, f)})


def remember_sent(item):
    str_id = "{}_{}".format(item['post_id'], item['source_id'])

    item_date = datetime.datetime.fromtimestamp(item['date'])
    today_dir = "mem/%d-%d-%d" % (item_date.year, item_date.month, item_date.day)

    if not os.path.isdir(today_dir):
        os.mkdir(today_dir)

    with open(today_dir + "/" + str_id, 'w') as f:
        pass

    item_date_yest = datetime.datetime.fromtimestamp(item['date'] - (86400 * 2))
    yest_dir = "mem/%d-%d-%d" % (item_date_yest.year, item_date_yest.month, item_date_yest.day)

    try:
        shutil.rmtree(yest_dir)
    except OSError as e:
        # print(e)
        pass


def check_sent(item):
    str_id = "{}_{}".format(item['post_id'], item['source_id'])

    item_date = datetime.datetime.fromtimestamp(item['date'])
    today_dir = "mem/%d-%d-%d" % (item_date.year, item_date.month, item_date.day)

    return os.path.isfile(today_dir + "/" + str_id)


def all_images(item):
    if 'attachments' in item:
        for a in item['attachments']:
            if not a['type'] == 'photo':
                return False
        return True
    return False


def sanitize(sss: str):
    sss = sss.replace('<br>', '\n')

    return sss


for item in news['items']:

    if not item['type'] == 'post':
        continue
    if check_sent(item):
        continue
    if 'https://vk.com/' in item['text']:
        continue
    if '[club' in item['text']:
        continue
    if 'post_type' in item and item['post_type'] == 'copy':
        continue
    if 'marked_as_ads' in item and item['marked_as_ads']:
        continue
        
    time.sleep(3)

    # bot.send_message(chat_id='@memesFromKvis', text=item['text'])

    if 'text' in item:
        item['text'] = sanitize(item['text'])

    if 'attachments' in item and len(item['attachments']) == 1:
        atch = item['attachments'][0]

        if atch['type'] == 'doc' and atch['doc']['ext'] in IGNORE_EXT:
            pass
        elif atch['type'] == 'photo':

            im = Image.open(requests.get(atch['photo']['src_big'], stream=True).raw)
            imgByteArr = io.BytesIO()
            im.save(imgByteArr, 'JPEG')
            imgByteArr.seek(0)

            caption = item['text']

            if len(caption) > 200:
                bot.send_message(text=caption, chat_id=CHAT_ID)
                caption = ''

            bot.send_photo(chat_id=CHAT_ID, caption=caption, photo=imgByteArr)
            remember_sent(item)
            # break

        elif atch['type'] == 'doc' and atch['doc']['ext'] == 'gif':
            im = requests.get(atch['doc']['url'], stream=True)
            imgByteArr = io.BytesIO(im.content)

            imgByteArr.seek(0)
            caption = item['text']
            if len(caption) > 200:
                bot.send_message(text=caption, chat_id=CHAT_ID)
                caption = ''

            upload_doc(imgByteArr, caption)
            remember_sent(item)

            # break

        elif atch['type'] == 'video' and 'platform' in atch['video'] and atch['video']['platform'] == 'YouTube':

            video = api.video.get(videos='{}_{}'.format(atch['video']['owner_id'], atch['video']['vid']))

            im = Image.open(requests.get(atch['video']['image_big'], stream=True).raw)
            imgByteArr = io.BytesIO()
            im.save(imgByteArr, 'JPEG')
            imgByteArr.seek(0)

            bot.send_photo(chat_id=CHAT_ID, caption=video[1]['player'], photo=imgByteArr)
            remember_sent(item)
            # break
        else:
            print("CASE 1")
            pprint.pprint(item)
    else:
        if 'attachments' not in item:
            bot.send_message(text=item['text'], chat_id=CHAT_ID)
            remember_sent(item)

        elif all_images(item):
            images = []
            for attach in item['attachments']:
                im = Image.open(requests.get(attach['photo']['src_big'], stream=True).raw).convert('RGB')
                images.append(im)

            min_shape = sorted([(np.sum(i.size), i.size) for i in images])[0][1]

            imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in images))
            imgs_comb = Image.fromarray(imgs_comb)

            imgByteArr = io.BytesIO()
            imgs_comb.save(imgByteArr, 'JPEG')
            imgByteArr.seek(0)

            width, height = imgs_comb.size

            caption = item['text']

            if len(caption) > 200:
                bot.send_message(text=caption, chat_id=CHAT_ID)
                caption = ''

            if (width / height) > 2:
                upload_doc(imgByteArr, caption, 'file.jpg')
            else:
                bot.send_photo(chat_id=CHAT_ID, caption=caption, photo=imgByteArr)

            remember_sent(item)

        else:
            # print("CASE 2")
            # pprint.pprint(item)
            pass
