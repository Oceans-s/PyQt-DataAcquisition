import random
import re
import time
import more_itertools
import requests
import os
import sys

from multiprocessing.pool import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_url(det):
    driver = webdriver.Chrome()
    pattern = re.compile(r'img.*ng-src="(.*?)"')  # 正则表达式匹配原图url
    base_url = "https://openi.nlm.nih.gov/"
    driver.get(base_url + det)
    time.sleep(3) #等待网页加载，负责会出现获取不到网页信息的情况
    img_tag = driver.find_element(By.CLASS_NAME, "image.ng-scope").get_attribute("outerHTML")
    match = re.findall(pattern, img_tag)  # 获得所有原图url
    real_url = base_url + match[0]
    driver.quit()
    return real_url


def get_page(tot):
    if tot <= 100:
        page = [0]
    elif 100 < tot <= 1000:
        count = int(tot / 100) + 1
        page = random.sample(range(0, count), count)
    elif 1000 < tot <= 5000:
        count = 10
        page = random.sample(range(0, count), 10)
    else:
        page = random.sample(range(0, 51), 10)

    return page


def get_path(path):
    temp = path.split("/")
    real_path = ""
    for i in range(0, len(temp)):

        real_path += temp[i]
        if i != len(temp) - 1:
            real_path += "//"

    return real_path


class Img:
    text = None
    path = None

    def get_detail(self, index):
        driver = webdriver.Chrome()
        # 控制浏览器访问url地址
        m = index * 100 + 1
        n = m + 99
        search_url = "https://openi.nlm.nih.gov/gridquery?q={}&m={}&n={}".format(self.text, m, n)
        driver.get(search_url)
        time.sleep(3) #等待网页加载，负责会出现获取不到网页信息的情况
        tag = driver.find_element(By.ID, "grid").get_attribute("outerHTML")  # 找到定位标签对
        pattern = re.compile(r'a.*ng-href="(.*?)"')  # 正则表达式匹配原图所在网页url
        match = re.findall(pattern, tag)  # 获得所有原图所在网页url
        # time.sleep(1)
        driver.quit()
        return match

    def get_img(self, url):
        os.chdir(self.path)
        img_name = url.split("/")[-1].split("?")[0]
        resp = requests.get(url)  # 获取网页信息
        byte = resp.content  # 转化为content二进制
        with open(img_name, "wb") as f:  # 文件写入
            f.write(byte)

    def set_text(self, text):
        self.text = text

    def set_path(self, path):
        self.path = path


if __name__ == '__main__':
    inputText = sys.argv[1]
    numText = int(sys.argv[2])
    total = int(sys.argv[3])
    filePath = sys.argv[4]

    print(inputText, numText, total, filePath)

    # start = time.perf_counter()

    img = Img()
    img.set_text(inputText)
    img.set_path(get_path(filePath))

    pool = Pool(processes=10)

    try:
        # print("Getting web page information...")
        detail = list(more_itertools.collapse(pool.map(img.get_detail, get_page(total))))

        # print("Getting an image link...")
        imgUrl = pool.map(get_url, random.sample(detail, int(numText)))

        # print("Downloading pictures...")
        pool.map(img.get_img, imgUrl)

        print("Images download completed!")
        pool.close()
        pool.join()

        # end = time.perf_counter()
        # print('Running time: %s Seconds' % (end - start))

    except:
        print("Something went wrong...[MyUrl.py]")
