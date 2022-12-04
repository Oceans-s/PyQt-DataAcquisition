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
    pattern = re.compile(r'img.*ng-src="(.*?)"')  # The regular expression matches the original image url
    base_url = "https://openi.nlm.nih.gov/"
    driver.get(base_url + det)
    time.sleep(3)  # Waiting for the page to load, responsible for the failure to obtain the page information
    img_tag = driver.find_element(By.CLASS_NAME, "image.ng-scope").get_attribute("outerHTML")
    match = re.findall(pattern, img_tag)  # Get all original image urls
    real_url = base_url + match[0]
    driver.quit()
    return real_url


def get_page(tot):

    """Determine the number of pages to crawl based on the total number of results found"""
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

    """Get correct save path"""
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
        # Control the url access of the browser
        m = index * 100 + 1
        n = m + 99
        search_url = "https://openi.nlm.nih.gov/gridquery?q={}&m={}&n={}".format(self.text, m, n)
        driver.get(search_url)
        time.sleep(3)  # Waiting for the page to load, responsible for the failure to obtain the page information
        tag = driver.find_element(By.ID, "grid").get_attribute("outerHTML")  # Locate the locator tag pair
        pattern = re.compile(r'a.*ng-href="(.*?)"')  # The regular expression matches the url of the page where the
        # original image resides
        match = re.findall(pattern, tag)  # Get the url of the page where all the original images are located
        # time.sleep(1)
        driver.quit()
        return match

    def get_img(self, url):
        os.chdir(self.path)
        img_name = url.split("/")[-1].split("?")[0]
        resp = requests.get(url)  # Get Web Information
        byte = resp.content  # Convert to content binary
        with open(img_name, "wb") as f:  # File writing
            f.write(byte)

    def set_text(self, text):
        self.text = text

    def set_path(self, path):
        self.path = path


if __name__ == '__main__':
    """Get the param"""
    inputText = sys.argv[1]
    numText = int(sys.argv[2])
    total = int(sys.argv[3])
    filePath = sys.argv[4]

    print(inputText, numText, total, filePath)

    # start = time.perf_counter()

    img = Img()
    img.set_text(inputText)  # set the search content
    img.set_path(get_path(filePath))  # set the save path

    pool = Pool(processes=10)  # Enabling a Process Pool

    try:
        # print("Getting web page information...")
        detail = list(more_itertools.collapse(pool.map(img.get_detail, get_page(total))))   # get detailed page's url

        # print("Getting an image link...")
        imgUrl = pool.map(get_url, random.sample(detail, int(numText)))  # get all original images' url

        # print("Downloading pictures...")
        pool.map(img.get_img, imgUrl)  # download all images

        print("Images download completed!")
        pool.close()
        pool.join()

        # end = time.perf_counter()
        # print('Running time: %s Seconds' % (end - start))

    except:
        print("Something went wrong...[MyUrl.py]")
