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


def main():
    print('argv[1]: save location (filepath)')
    print('argv[2]: path of chromedriver appropriate for installed chrome version')
    print('argv[3]: number of pages to search')
    print('argv[4] and beyond: search terms (can use spaces, put "site:" before a site-specific search')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options, executable_path=sys.argv[2])

    keyword = ''
    filename = ''

    for i in range(4, len(sys.argv)):
        keyword += sys.argv[i]

        if sys.argv[i].startswith('site:'):
            sys.argv[i] = sys.argv[i][5:len(sys.argv[i])]

        filename += sys.argv[i]

        if i != len(sys.argv) - 1:
            keyword += ' '
            filename += '_'

    filename += '_' + 'pn=' + sys.argv[3] + '_' + time.strftime("%Y%m%d%H%M", time.localtime())
    filename += ".csv"

    savefolder = sys.argv[1]
    allfiles = os.listdir(savefolder)

    links = set([])

    for file in allfiles:
        if file.endswith('.csv'):
            partition = file[0:file.find('_pn')]
            if partition == filename[0:file.find('_pn')]:
                filepath = os.path.join(sys.argv[1], file)
                openfile = open(filepath, 'r', encoding='utf-8')

                openfile.readline()
                openfile.readline()

                content = openfile.readline()
                while content is not '':
                    try:
                        urltemp = content.split(',')[1]
                        url = urltemp[0:len(urltemp) - 1]
                        links.add(url)
                        content = openfile.readline()
                    except:
                        content = openfile.readline()
                        pass

    savepath = os.path.join(sys.argv[1], filename)
    f = open(savepath, 'w', encoding='utf-8')
    print(filename, file=f)

    print("Title,Link", file=f)
    print("WEB RESULTS", file=f)

    searchfirst = "http://www.baidu.com/s?wd=" + quote(keyword)
    browser.get(searchfirst)
    firstpage = BeautifulSoup(browser.page_source, 'lxml')
    numStr = firstpage.find('span', class_='nums_text').get_text()
    numStr = numStr.replace(',', '')
    numofres = int(numStr[11:len(numStr) - 1])

    for i in range(0, int(sys.argv[3]) * 10 if int(sys.argv[3]) * 10 < numofres else numofres, 10):

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
                if actualUrl.startswith('http') and not links.__contains__(actualUrl):
                    links.add(actualUrl)
                    print(h3.get_text().replace(',', ' ').replace('\n', '') + ',' + actualUrl, file=f)
            except:
                pass
        time.sleep(1)

    print("MOBILE RESULTS", file=f)

    for i in range(0, int(sys.argv[3]) * 10 if int(sys.argv[3]) * 10 < numofres else numofres, 10):

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
                        link = link[0:len(link) - 1]
                    if not links.__contains__(link):
                        print(a.get_text().replace(',', ' ').replace('\n', '') + ',' + link, file=f)
                except:
                    pass

    browser.quit()
    f.close()


if __name__ == '__main__':
    main(sys.argv)
