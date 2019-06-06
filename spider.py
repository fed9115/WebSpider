from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import sys
import os.path

'''
    This Python script is designed as a web spider to get search results from baidu.com, which is the biggest search 
engine in China.
    By using this program, user can get the results (at most 30) of the keyword in first 3 pages. The program can 
generate a txt file which contains at most 60 lines. For each searching result, first line is the title of it, and the 
second line is the link. 
    This Program only supports Python with version over 3, so it does not support Python 2. Before using it, user must 
make sure s/he has the driver of the browser in the computer to run the web spider. (Actually the spider is an 
artificial visit and it can avoid the anti-spider mechanism of the search engine by opening a new page in the specified 
browser). The developers provide web drivers of Chrome 74 on Linux, MacOS, and Windows under the folder venv. 
    This program can be run in cmd (a.k.a. terminal on Linux and Mac). When executing it, user must pass at least 3 
parameters, the first one is the path of the save txt file, the second one is the path of the web driver, the following
ones are the keywords the user would like to search. The user can designate a specific website, if do so, the searching 
results will only be consist of the web pages under the site. For example, if you would like to search documents under 
百度文库(Baidu Wenku), you may append a token after your keyword like "site:wenku.baidu.com." Remember to add the 
required identifier "site:". In a nutshell, for example, you want to search a product called iPhone of the company 
called Apple under Baidu Wenku by using Chrome 74 on Mac, and you want to generate the resulting file on Desktop,
you may type /Users/**userName**/Desktop/ chromedriver-Mac iPhone Apple site:wenku.baidu.com

@author Max Chen, Erdi Fan

@version 19.6.4
'''


def main(argv):
    browser = webdriver.Chrome(argv[2])

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
            print(h3.get_text().replace(',', ' ').replace('\n', '') + ',' + a['href'], file=f)

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
                print(a.get_text().replace(',', ' ').replace('\n', '') + ',' + a['href'], file=f)

        time.sleep(1)

    browser.quit()
    f.close()


if __name__ == '__main__':
    main(sys.argv)
