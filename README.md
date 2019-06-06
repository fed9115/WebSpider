# WebSpider
    This Python script is designed as a web spider to get search results from baidu.com, which is the biggest search engine in China.
    By using this program, user can get the results of. The program can generate a csv file which contains at most 60 lines. For each searching result, first line is the title of it, and the second line is the link. 
    This Program only supports Python with version over 3, so it does not support Python 2. Before using it, user must make sure s/he has the driver of the browser in the computer to run the web spider. (Actually the spider is an artificial visit and it can avoid the anti-spider mechanism of the search engine by opening a new page in the specified browser). The developers provide web drivers of Chrome 74 on Linux, MacOS, and Windows under the folder venv. 
    This program can be run in cmd (a.k.a. terminal on Linux and Mac). When executing it, user must pass at least 4 parameters, the first one is the path of the save txt file, the second one is the path of the web driver, the third one is how many pages of results in baidu.com (10 results per page) you want to get, and the following
ones are the keywords the user would like to search. The user can designate a specific website, if do so, the searching results will only be consist of the web pages under the site. For example, if you would like to search documents under 百度文库(Baidu Wenku), you may append a token after your keyword like "site:wenku.baidu.com." Remember to add the required identifier "site:". In a nutshell, for example, you want to search a product called iPhone of the company called Apple under Baidu Wenku by using Chrome 74 on Mac for 4 pages (40 results), and you want to generate the resulting file on Desktop, you may type /Users/**userName**/Desktop/ chromedriver-Mac 4 iPhone Apple site:wenku.baidu.com
