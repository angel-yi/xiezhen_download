"""
下载wxept网站中的图片
"""
import random
import time

import requests
from loguru import logger
from lxml import etree
from retry import retry

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
    , 'referer': 'https://www.meitu131.net/'
}
PROXY = {'http': 'http://127.0.0.1:33210', 'https': 'http://127.0.0.1:33210'}
f = open('img_urls_wxept.txt', 'a', encoding='utf-8')

logger.add('wxept.log')

@retry()
def parse_img(html):
    html = etree.HTML(html)
    img_url = html.xpath('/html/body/section/article/p/a/img/@src')
    logger.info(img_url)
    for img in img_url:
        f.write(f'{img}\n')
        f.flush()


@retry()
def parse_html(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    parse_img(resp.text)
    html = etree.HTML(resp.text)
    pages = html.xpath('/html/body/section/div[1]/a/span/text()')[-1]
    page_numbers = str(pages)
    for i in range(2, int(page_numbers)):
        other_page = f'{url}/{i}'
        logger.info(f'[other page] {other_page}')
        resp = requests.get(other_page, headers=HEADERS, proxies=PROXY, timeout=10)
        parse_img(resp.text)
        time.sleep(random.random())


@retry(tries=5, delay=3)
def parse_page(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    html = etree.HTML(resp.text)
    html_urls = html.xpath('/html/body/section/div[3]/div/article/a/@href')
    logger.info(html_urls)
    for html_url in html_urls:
        logger.info(f'[get html] {html_url} [page] {url}')
        parse_html(html_url)
        time.sleep(random.randint(3, 5))


if __name__ == '__main__':
    for page in range(164, 1434):
        # 117
        url = f'https://www.wxept.com/page/{page}'
        logger.info(f'[get page] {page} {url}')
        try:
            parse_page(url)
        except:
            continue
