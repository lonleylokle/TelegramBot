import re

import requests
from bs4 import BeautifulSoup as BS

cities = {}

def parse_cities():
    myUrl = "https://www.kassir.ru/"
    res = requests.get(myUrl)
    html = BS(res.content, 'html.parser')

    for tag in html.find_all('li'):
        tag = tag.find('a')
        cities[tag.text] = tag.get('href')


def parser_search(search_text):
    l1 = []
    category = 'category'
    city = 'Москва'
    payload = {'keyword': search_text}
    myUrl = cities[city] + '/' + category
    res = requests.get(myUrl, params=payload)
    print(res)
    html = BS(res.content, 'html.parser')
    for tag in html.select('.caption'):
        img = tag.parent.find('img').get('data-src')
        tag = tag.contents
        if len(tag[3]) > 1:
            tag[3].contents[0] += tag[3].contents[1].string
        # str1 = re.search(r'http.*g\"', tag[7].contents[1].get('data-ec-item')).group(0) + '\n'
        str1 = '[Ссылка]['
        str1 += tag[1].find('a').get('href') + ']'
        str1 += '\n' + tag[1].string + '\n'
        str1 += re.sub(r'\s*\B', '', tag[3].contents[0]) + '\n '
        str1 += re.sub(r'\s*\B', '', tag[5].contents[0]) + '\n'
        str1 += re.sub(r'\s*\B', '', tag[9].text)
        l1.append([img, str1])
    print(l1)
    return l1


# myUrl = 'https://msk.kassir.ru/festivali/aerodrom-chyornoe/festival-nebo-teoriya-i-praktika_2020-05-23'
# res = requests.get(myUrl)
# html = BS(res.content, 'html.parser')
#
# for i in html.select('.full'):
#     for j in range(len(i.find_all('p'))):
#         print(i.find_all('p')[j].text)
#
# for i in html.select('.apply-owl-carousel'):
#     for j in range(len(i.find_all('img'))):
#         print(i.find_all('img')[j].get('src'))