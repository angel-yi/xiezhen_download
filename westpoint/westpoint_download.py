"""
下载暴恐图片
"""
import hashlib
import os
import time

import requests
from loguru import logger
from lxml import etree
from retry import retry

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77 '
}

save_path = r"C:\Users\Administrator\Desktop\xz_classifer\暴恐"

@retry()
def download_img(img_url, img_name):
    resp = requests.get(img_url, headers=headers, timeout=10,
                        proxies={'http': 'http://127.0.0.1:33210', 'https': 'http://127.0.0.1:33210'})
    logger.info(resp)
    if resp.status_code == 200:
        with open(os.path.join(save_path, img_name), 'wb') as f:
            f.write(resp.content)
            f.close()
    else:
        logger.error(f'{resp} 无法获取图片')

# @retry()
def main():
    for page in range(1, 41):
        logger.info(f'page [{page}/41]')
        url = f'https://ctc.westpoint.edu/militant-imagery-project/page/{page}/'
        resp = requests.get(url, headers=headers, timeout=10,
                            proxies={'http': 'http://127.0.0.1:33210', 'https': 'http://127.0.0.1:33210'})
        html = etree.HTML(resp.text)
        imgs = html.xpath('//*[@id="page"]/main/div[2]/div/div/div[1]/a/img/@src')
        for img in imgs:
            img_url = 'https://ctc.westpoint.edu/' + img
            img_ext = os.path.basename(img_url).split('.')[-1]
            img_name = hashlib.md5(str(img_url).encode(encoding='UTF-8')).hexdigest() + '.' + img_ext
            download_img(img_url, img_name)
            time.sleep(3)


if __name__ == '__main__':
    main()
