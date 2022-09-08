"""
根据图片url下载图片
"""
import hashlib
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from loguru import logger

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77',
    # 'referer': 'http://www.158nx.com/'
}


def get_img(img_url, save_path, nowi):
    logger.info(f'[{nowi}/{count}] [get]: {img_url} [name]: {save_path}')
    resp = requests.get(img_url, headers=headers, timeout=10,
                        proxies={'http': 'http://127.0.0.1:33210', 'https': 'http://127.0.0.1:33210'},
                        verify=False)
    logger.info(resp)
    if resp.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(resp.content)
            f.close()
    else:
        logger.error(f'{resp} 无法获取图片')


if __name__ == '__main__':
    urls = open(r'qinimg.txt', 'r', encoding='utf-8').readlines()
    urls = list(set(urls))
    # 从json文件读取
    # urls = json.load(open(r"C:\Users\Administrator\Desktop\crowl_images\危险pic_123rf2_terror.txt", 'r', encoding='utf-8'))['图片链接列表']
    save_dir = r"C:\Users\Administrator\Desktop\jh_dataset\qinimg"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    logger.info(f'共有{len(urls)}个图片链接')
    # 由于请求快导致网站断开连接，单线程慢慢抓
    pool = ThreadPoolExecutor(max_workers=10)

    old_md5s = os.listdir(save_dir)
    new_imgs_name = {}
    for i in range(len(urls)):
        url = urls[i].replace('\n', '')
        # logger.info(f'[{i}] [get url] {url}')
        img_ext = os.path.basename(url).split('.')[-1]
        img_name = hashlib.md5(str(url).encode(encoding='UTF-8')).hexdigest() + '.' + img_ext
        new_imgs_name[img_name] = url

    urls = list(set(new_imgs_name.keys()) - set(old_md5s))
    count = len(urls)
    for i in range(len(urls)):
        # url = urls[i].replace('\n', '')
        url = new_imgs_name[urls[i]]
        logger.info(f'[get url] {url}')
        # img_ext = os.path.basename(url).split('.')[-1]
        # img_name = hashlib.md5(str(url).encode(encoding='UTF-8')).hexdigest() + '.' + img_ext
        # get_img(url, os.path.join(save_dir, img_name))
        # if img_name in old_md5s:
        #     continue
        img_name = urls[i]
        pool.submit(get_img, url, os.path.join(save_dir, img_name).replace('?ver=6', ''), i)
        time.sleep(random.random())
    pool.shutdown()
