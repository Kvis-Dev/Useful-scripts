# -*- coding: UTF-8 -*-
import datetime
import logging
import os
import pprint
import sys
import time
import urllib

import random
import string
import json

import telegram
import vk
from PIL import Image, ImageDraw
import requests
import io
import imageio

import shutil

from telegram import InputFile

class Bot2(telegram.Bot):
    def send_media_group(self, chat_id, media, caption, *args, **kwargs):
        url = '{0}/sendMediaGroup'.format(self.base_url)

        media_f = []
        for i, f in enumerate(media):
            media_f.append({
                "type":"photo",
                "media":'attach://file-%s' % i,
                "caption": caption
            })

        data = {'chat_id': chat_id, 'media': json.dumps(media_f)}

        if caption:
            data['caption'] = caption

        return url, data

def to_media_form(data, files):
    form = []
    form_boundary = '--' + files[0].boundary

    for name in iter(data):
        value = data[name]
        form.extend([
            form_boundary, 'Content-Disposition: form-data; name="%s"' % name, '', str(value)
        ])


    for i, file in enumerate(files):
        form.extend([
            form_boundary, 'Content-Disposition: form-data; name="%s"; filename="%s"' %
                           ('file-%s'%i, file.filename),
                           'Content-Type: %s' % file.mimetype, '', file.input_file_content
        ])

    form.append('--' + files[0].boundary + '--')
    form.append('')

    return files[0].headers, InputFile._parse(form)


logger = logging.getLogger('vk')
logger.setLevel(logging.DEBUG)
APP_ID = 12345678
CHANNEL = '<vk channel name>'
CHAT_ID = '@chat_id'
BOT_TOKEN = '00000000000000000000000000'

IGNORE_EXT = ['srt', 'doc']

bot = Bot2(BOT_TOKEN)

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


def images_to_gif(urls):
    images = []

    for im_url in urls:
        im = Image.open(requests.get(im_url, stream=True).raw)
        # imgByteArr = io.BytesIO()
        # im.save(imgByteArr, 'JPEG')
        # imgByteArr.seek(0)
        #
        # images.append(imageio.imread(imgByteArr))
        images.append(im)

    max_w = 0
    max_h = 0

    for image in images:
        # print(image, image.size, image.shape, type(image))
        width, height = image.size
        if width > max_w:
            max_w = width
        if height > max_h:
            max_h = height

    if max_w > 1280:
        max_w = 1280

    if max_h > 1280:
        max_h = 1280

    new_images = []
    ii = 0
    for image in images:
        bigim = Image.new("RGB", (max_w, max_h), (255, 255, 255))
        img = image
        width, height = image.size

        new_width_c1 = max_w
        new_height_c1 = new_width_c1 * height / width

        new_height_c2 = max_h
        new_width_c2 = new_height_c2 * width / height

        if (width / height) > (max_w / max_h):
            new_width = new_width_c1
            new_height = new_height_c1
        else:
            new_width = new_width_c2
            new_height = new_height_c2

        img = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
        bigim.paste(img, (int((max_w - new_width) / 2), int((max_h - new_height) / 2)))

        circle_w = max_h / 100 * 2
        draw = ImageDraw.Draw(bigim)

        for i in range(len(images)):
            x = (max_w * 0.2) + (((max_w * 0.8) / len(images)) * i) - circle_w/2
            if ii == i:
                fill = 'red'
                outline = 'white'
            else:
                outline = 'black'
                fill = 'white'
            draw.ellipse((x, circle_w, x + circle_w, circle_w + circle_w), outline=outline, fill=fill)
        ii += 1
        new_images.append(bigim)

    save_imgs = []
    for image in new_images:
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, 'JPEG')
        imgByteArr.seek(0)
        save_imgs.append(imageio.imread(imgByteArr))

    imgByteArr = io.BytesIO()
    # kwargs_write = {'fps': 5.0, 'quantizer': 'nq'}
    imageio.mimsave(imgByteArr, save_imgs, format='GIF', duration=2)
    imgByteArr.seek(0)
    return imgByteArr


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
            # urls = []
            # for attach in item['attachments']:
            #     urls.append(attach['photo']['src_big'])

            # f = images_to_gif(urls)
            caption = item['text']

            if len(caption) > 200:
                bot.send_message(text=caption, chat_id=CHAT_ID)
                caption = ''

            # upload_doc(f, caption)

            # remember_sent(item)
            media_files = []
            for attach in item['attachments']:
                im = Image.open(requests.get(attach['photo']['src_big'], stream=True).raw)
                imgByteArr = io.BytesIO()
                im.save(imgByteArr, 'JPEG')
                imgByteArr.seek(0)

                ifile = InputFile({'photo': imgByteArr})
                media_files.append(ifile)

            url, data = bot.send_media_group(chat_id=CHAT_ID, caption=caption, media=media_files)
            headers, mform = to_media_form(data, media_files)
            bot._request._request_wrapper('POST', url, body=mform, headers=headers)
            # remember_sent(item)

        else:
            # print("CASE 2")
            # pprint.pprint(item)
            pass
