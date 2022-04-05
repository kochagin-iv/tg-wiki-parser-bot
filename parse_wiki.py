from bs4 import BeautifulSoup
import requests
import re

str_full_text = list()
used_links = []


def get_str_full_text():
    global str_full_text
    return str_full_text


def get_html(url):
    r = requests.get(url).text
    return r


def parse(url, depth):
    if 'https://en.wikipedia.org/' not in url:
        return
    global str_full_text
    global used_links
    html = get_html(url)
    if requests.get(url).status_code != 200:
        return
    used_links.append(url)
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a', href=True)
    if depth > 1:
        for i in links:
            if i["href"] in used_links:
                continue
            used_links.append(i["href"])
            if 'https:' not in i['href']:
                parse('https://en.wikipedia.org/' + i['href'], depth - 1)
            else:
                parse(i['href'], depth - 1)

    p = soup.find('div', id = 'bodyContent')
    if p is None:
        return
    arr = p.getText()
    arr = str(arr)
    str_full_text += re.findall(r'\w+', arr)
