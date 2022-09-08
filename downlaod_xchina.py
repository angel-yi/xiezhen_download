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
    # , 'referer': 'https://www.meitu131.net/'
}
PROXY = {'http': 'http://127.0.0.1:33210', 'https': 'http://127.0.0.1:33210'}
name = 'xchina2'
f = open(f'{name}.txt', 'a', encoding='utf-8')

logger.add(f'{name}.log')

@retry()
def parse_img(html):
    html = etree.HTML(html)
    img_url = html.xpath('/html/body/div[5]/div[3]/div/div/a/img/@src')
    logger.info(img_url)
    for img in img_url:
        f.write(f'{img}\n')
        f.flush()


@retry()
def parse_html(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    parse_img(resp.text)
    html = etree.HTML(resp.text)
    pages = html.xpath('//*[@id="pages"]/a/text()')[-2]
    page_numbers = str(pages)
    for i in range(2, int(page_numbers)):
        other_page = url.replace('.html', f'_{i}.html')
        logger.info(f'[other page] {other_page}')
        resp = requests.get(other_page, headers=HEADERS, proxies=PROXY, timeout=10)
        parse_img(resp.text)
        time.sleep(random.random())


@retry()
def parse_page(url):
    resp = requests.get(url, headers=HEADERS, proxies=PROXY, timeout=10)
    html = etree.HTML(resp.text)
    html_urls = html.xpath('/html/body/div[8]/div/div/div[2]/div[4]/div[2]/div/div[1]/a/video/@poster')
    logger.info(html_urls)
    for html_url in html_urls:
        # logger.info(f'[get html] {html_url} [page] {url}')
        # parse_html(html_url)
        # time.sleep(random.randint(3, 5))
        f.write('https://xchina.co/'+f'{html_url}\n')
        f.flush()

if __name__ == '__main__':
    for page in range(1, 338):
        # 117
        url = f'https://xchina.co/videos/series-%E5%9B%BD%E4%BA%A7AV/{page}.html'
        logger.info(f'[get page] {page} {url}')
        parse_page(url)
        random.randint(1, 3)
