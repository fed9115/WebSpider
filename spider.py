from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import sys
import os.path
import requests

'''
@author Max Chen, Erdi Fan

@version 19.6.10
'''


def main(argv):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path=argv[2])

    keyword = ''
    filename = ''

    for i in range(4, len(sys.argv)):
        keyword += argv[i]
        filename += argv[i]
        if i != len(sys.argv) - 1:
            keyword += ' '
            filename += '_'

    filename += '_' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename += ".csv"

    savepath = os.path.join(argv[1], filename)

    f = open(savepath, 'w', encoding='utf-8')

    print("Title,Link", file=f)
    print("WEB RESULTS", file=f)

    for i in range(0, int(argv[3]) * 10, 10):

        page = str(0 + i)

        url_web = "http://www.baidu.com/s?wd=" + quote(keyword) + '&pn=' + quote(page)

        browser.get(url_web)

        soup_web = BeautifulSoup(browser.page_source, 'lxml')

        res_web = soup_web.find_all('h3')

        for h3 in res_web:
            a = h3.find('a', href=True)
            fakeUrl = a['href']
            try:
                actualUrl = requests.get(fakeUrl, allow_redirects=False).headers['Location']
                if actualUrl.startswith('http'):
                    print(h3.get_text().replace(',', ' ').replace('\n', '') + ',' + actualUrl, file=f)
            except:
                pass
        time.sleep(1)

    print("MOBILE RESULTS", file=f)


    for i in range(0, int(argv[3]) * 10, 10):

        page = str(0 + i)

        url_mobile = 'http://m.baidu.com/s?pn=' + quote(page) + '&word=' + quote(keyword)

        browser.get(url_mobile)

        soup_mobile = BeautifulSoup(browser.page_source, 'lxml')

        res_mobile = soup_mobile.find_all('header')

        for header in res_mobile:
            a = header.find('a', href=True)
            if a is not None:
                fakeUrl = requests.get(a['href']).url

                try:
                    actual = requests.get(fakeUrl, allow_redirects=False)
                    soup_link = BeautifulSoup(actual.content, 'lxml')
                    link = object.__str__(soup_link.find('noscript').find())
                    link = link[22:len(link) - 24]
                    if link.endswith('\''):
                        link = link[0:len(link)-1]
                    print(a.get_text().replace(',', ' ').replace('\n', '') + ',' + link, file=f)
                except:
                    pass

    browser.quit()
    f.close()


if __name__ == '__main__':
    main(sys.argv)
