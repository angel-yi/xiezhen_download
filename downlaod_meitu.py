"""
下载meitu131网站中的图片
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
f = open('img_urls.txt', 'w', encoding='utf-8')


@retry()
def parse_img(html):
    html = etree.HTML(html)
    img_url = html.xpath('//*[@id="main-wrapper"]/div[2]/p/a/img/@src')
    logger.info(img_url)
    f.write(f'{img_url[0]}\n')
    f.flush()


@retry()
def parse_html(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    parse_img(resp.text)
    html = etree.HTML(resp.text)
    pages = html.xpath('//*[@id="pages"]/a[1]/text()')[0]
    page_numbers = str(pages).split('/')[1]
    for i in range(2, int(page_numbers)):
        other_page = f'{url}/index_{i}.html'
        logger.info(f'[other page] {other_page}')
        resp = requests.get(other_page, headers=HEADERS, proxies=PROXY, timeout=10)
        parse_img(resp.text)
        time.sleep(random.random())


@retry()
def parse_page(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    html = etree.HTML(resp.text)
    html_urls = html.xpath('/html/body/div[1]/div[2]/ul/li/div[1]/a/@href')
    logger.info(html_urls)
    for html_url in html_urls:
        logger.info(f'[get html] https://www.meitu131.com{html_url}')
        parse_html('https://www.meitu131.com' + html_url)
        time.sleep(random.randint(3, 5))


if __name__ == '__main__':
    for page in range(158):
        # 117
        url = f'https://www.meitu131.com/e/search/result/index.php?page={page}&searchid=186'
        logger.info(f'[get page] {page} {url}')
        parse_page(url)
