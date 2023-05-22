import time

import requests
from lxml import etree
def savePhotos(img_url, os_path):
    img_res = requests.get(img_url)
    print("正在下载图片%s"%os_path[-10:])
    with open(os_path, mode='wb+') as f:
        f.write(img_res.content)

# 更改start_page 和end_page 可以控制爬取页面范围
start_page = 1
end_page = 10

for page in range(start_page,end_page):
    print("---------------正在解析第%d页----------------"%page)
    url = "https://wallhaven.cc/search?categories=111&purity=000&atleast=1600x1200&sorting=hot&order=desc&ai_art_filter=1&page=%d" % page
    try:
        res = requests.get(url)
    except:
        print("异常, 睡眠三秒")
        time.sleep(3)
        res = requests.get(url)
    tree = etree.HTML(res.text)
    count = 0
    try:
        img_list = tree.xpath("/html/body/main/div[1]/section[1]/ul/li")
    except:
        print("页面解析异常，正在获取下一页面")
        continue

    for img in img_list:
        href = img.xpath("figure/a/@href")[0]
        # 获取到第二层界面
        photo_name = href[-6:]
        try:
            img_html_tree = etree.HTML(requests.get(href).text)
            img_href = img_html_tree.xpath("/html/body/main/section/div[1]/img/@src")[0]
        except:
            continue
        try:
            savePhotos(img_href, "Wall Papers/%s.png" % photo_name)
        except:
            print("图片下载异常, 下一张图片")
            continue
