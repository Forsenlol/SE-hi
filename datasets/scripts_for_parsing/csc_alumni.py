import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from time import sleep

csc_url = 'https://compscicenter.ru/alumni/'

driver = webdriver.Chrome(
    executable_path='/Users/vladiknaska/Documents/se/chromedriver')

driver.get(csc_url)

# change courses
driver.find_element_by_class_name('col-lg-3.mb-4').click()
sleep(3)
driver.find_element_by_id('react-select-3-option-2').click()


# change year
def get_page_by_year(year_option):
    '''
    0 - 2019
    1 - 2018
    ...
    6 - 2013
    '''

    driver.find_element_by_class_name(
        'react-select__control.css-yk16xz-control').click()
    sleep(1)
    driver.find_element_by_id(f'react-select-2-option-{year_option}').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    return driver.page_source


urls = []
for i in range(7):
    try:
        html_source = get_page_by_year(i)
        soup = BeautifulSoup(html_source, 'html.parser')
        base = 'https://compscicenter.ru'
        for card in soup.find_all('a', {'class': 'card _user'}):
            urls.append(base + card['href'])
        sleep(3)
    except:
        print(i)

feedback, img, stud_names, course_list = [], [], [], []

for url in urls:
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    stud_names.append(soup.find('h1', {'class': 'mb-0'}).text)

    feedback.append(soup.find('p').text)
    img.append('https://compscicenter.ru' + soup.find('img')['src'])

    course_names = []
    marks = []
    for div in soup.find_all('div', {'class': 'timeline__content'}):
        for ul in div.find_all('ul', {'class': 'ui'}):
            for li in ul.find_all('li'):
                try:
                    course_names.append(li.a.text)
                except:
                    course_names.append(li.text)
                marks.append(li.span.text)

    course_list.append(
        {k.strip(): v.strip() for k, v in zip(course_names, marks)})

df = pd.DataFrame({'name': stud_names, 'feedback': feedback,
                   'img': img, 'courses': course_list, 'url': urls})

df.loc[df.feedback == 'Отправил заявление', 'feedback'] = None
df.loc[df.feedback == 'Отправила заявление', 'feedback'] = None

path = 'csc_photos'
for idx in range(len(df)):
    img_data = requests.get(df.img[idx]).content
    with open(os.path.join(path, f'{df.name[idx].split()[1]}.png'),
              'wb') as handler:
        handler.write(img_data)

df.to_csv('csc')