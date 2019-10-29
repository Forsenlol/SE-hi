import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

base = 'http://mit.spbau.ru'

r = requests.get(base+'/students/se')
html = r.text

soup = BeautifulSoup(html, 'html.parser')

names = []
images = []
hrefs = []
for div in soup.find_all('div', {'class': 'field-content alumni-userpic'}):
    for a in div.find_all('a'):
        names.append(a.text)
    for img in div.find_all('img'):
        images.append(img['src'])
        hrefs.append(base + a['href'])

df = pd.DataFrame({'name': [name for name in names if 0 < len(name.split()) < 5], \
                   'image': images, 'url': hrefs})

fields = ['field field-name-field-program field-type-list-text field-label-above',
         'field field-name-field-gradyead field-type-list-integer field-label-inline clearfix',
         'field field-name-field-thesistopic field-type-text field-label-above',
         'field field-name-field-advisor field-type-text field-label-above',
         'field field-name-field-wherenow field-type-text field-label-above',
         'field field-name-field-before-au field-type-text field-label-inline clearfix']
image_class = 'field field-name-field-alumni-photo field-type-image field-label-hidden'

blocks = []
images = []
for url in df.url:
    try:
        block = []
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        for field in fields:
            try:
                block.append(soup.find('div', {'class': field}).text)
            except:
                continue
        blocks.append(block)
        images.append(soup.find('div', {'class': image_class}).find('img')['src'])
    except:
        blocks.append([])
        images.append('None')
        print(url)


def get_info(block):
    dicts = [{k: v} for k, v in [line.split(':') for line in block]]
    info = dict(pair for d in dicts for pair in d.items())
    return info

infos = []
for block in blocks:
    infos.append(get_info(block))

df['info'] = infos

df['big_images'] = images

path = 'au_photos'
for idx in range(len(df)):
    if df.big_images[idx] != 'None':
        img_data = requests.get(df.big_images[idx]).content
    else:
        img_data = requests.get(df.image[idx]).content
    with open(os.path.join(path, f'{df.name[idx].split()[0]}.png'), 'wb') as handler:
        handler.write(img_data)

df.to_csv('au_students.csv')