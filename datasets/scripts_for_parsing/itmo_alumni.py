import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

itmo_url = 'http://mse.itmo.ru/alumni'

r = requests.get(itmo_url)
soup = BeautifulSoup(r.text, 'html.parser')

titles = []
names = []
images = []
for title, name, image in zip(soup.find_all('div', {'class': 't214__descr t-text'}),
               soup.find_all('div', {'class': 't214__title t-name t-name_sm'}),
               soup.find_all('meta', {'itemprop':'image'})):

    titles.append(title.text)
    names.append(name.text)
    images.append('http://mse.itmo.ru/' + image['content'])

df = pd.DataFrame({'name': names, 'titles': titles, 'images': images})

df.to_csv('itmo_students.csv')

path = 'itmo_photos'
for idx in range(len(df)):
    img_data = requests.get(df.images[idx]).content
    with open(os.path.join(path, f'{df.name[idx].split()[1]}.png'), 'wb') as handler:
        handler.write(img_data)