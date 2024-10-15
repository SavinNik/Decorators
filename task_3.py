import requests
import bs4
import re
from pprint import pprint
from urllib.parse import urljoin
import time

from logger_2 import logger

KEYWORDS = ['дизайн', 'фото', 'web', 'python']


@logger
def get_connection(url):
    try:
        response = requests.get(url)
        html = response.text
        return html
    except Exception as error:
        print(f'Ошибка соединения: {error}')

@logger
def get_pattern(list_of_words):
    pattern = r'\b(' + '|'.join(list_of_words) + r')\b'.lower()
    return pattern

@logger
def parse_articles(html, pattern, url):
    soup = bs4.BeautifulSoup(html, features='lxml')
    articles = soup.find_all('article', class_='tm-articles-list__item')

    parse_data = []

    for article in articles:
        try:
            link_tag = article.find('a', class_='tm-title__link')['href']
            link = urljoin(url, link_tag)
            date = article.find('time')['datetime']
            title_tag = article.find('a', class_='tm-title__link')
            title = title_tag.find('span').text.strip()

            if re.search(pattern, title.lower()):
                parse_data.append(f'{date} - {title} - {link}')
                continue

            html_article = get_connection(link)
            soup_article = bs4.BeautifulSoup(html_article, features='lxml')
            article_text = soup_article.find('div', id='post-content-body').text.lower()

            if re.search(pattern, article_text):
                parse_data.append(f'{date} - {title} - {link}')

            time.sleep(1)
        except AttributeError as error:
            print(f'Ошибка при парсинге: {error}')
            continue
    return parse_data


if __name__ == '__main__':
    URL = 'https://habr.com/ru/articles/'
    html_ = get_connection(URL)
    pattern_ = get_pattern(KEYWORDS)
    pprint(parse_articles(html_, pattern_, URL))

