from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import time
import os
import errno

start_time = time.time()

headers_list = [
    # Firefox 77 Mac
    {
        "User-Agent": 'Chrome/83.0.4103.97',
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        # "Chrome/83.0.4103.97 Safari/537.36",        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Firefox 77 Windows
    {
        "User-Agent": 'Chrome/83.0.4103.97',
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        # "Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
        "User-Agent": 'Chrome/83.0.4103.97',
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        # "Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows
    {
        "User-Agent": 'Chrome/83.0.4103.97',
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        # "Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.google.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
    }
]

ordered_headers_list = []
for headers in headers_list:
    h = OrderedDict()
    for header, value in headers.items():
        h[header] = value
    ordered_headers_list.append(h)


def url_scrapper(topic):
    #                            google url scrapping
    # ----------------------------------------------------------------------------------
    req = requests.get('https://www.google.com/search?q=' + topic.replace(' ', '+') + '&num=30',
                       headers=headers_list[0]).text
    soup = BeautifulSoup(req, "html.parser")
    links_a = soup.find_all('div', {'class': 'kCrYT'})  #

    links = []
    for link in links_a:
        try:
            cont = link.contents[0]['href']
            idx = cont.index('&sa=U&')
            cont = str(cont).replace(cont[idx:], '')
            cont = cont.replace('/url?q=', '')
            links.append(cont)
        except:
            pass

    return links


topic = input()
links = url_scrapper(topic)

for link in links:
    print(link)


def main_content_scrapper(url, j):
    def sub_content_scrapper(c_tag, f):
        def content_scrapper(p):
            for child in p.children:
                if type(child) == type(BeautifulSoup('<b><span>Dilshad</span></b>', 'html.parser').b):
                    content_scrapper(child)
                else:
                    try:
                        print('|-->  ', child)
                        f.write(child+'\n')
                    except UnicodeEncodeError:
                        pass
        if type(c_tag) == type(BeautifulSoup('<b>Dilshad</b>', 'html.parser').find_all('b')):
            for p in c_tag:
                content_scrapper(p)
        elif type(c_tag) == type(BeautifulSoup('<b><span>Dilshad</span></b>', 'html.parser').b):
            content_scrapper(c_tag)
        else:
            print('-->  ', type(c_tag), c_tag)
            # f.write(str(c_tag.encode('utf-8').decode('utf-8')) + '\n')
            f.write(c_tag + '\n')
    i = 0
    req = requests.get(url, headers=headers_list[i]).text
    f_name = "info/" + str(j) + "/"
    i += 1

    if i == 4: i = 0
    soup = BeautifulSoup(req, "html.parser")
    srch_tags = ['strong', 'b', 'h2', 'h3', 'ul', 'ol']
    c = 1
    for s_tag in srch_tags:
        filename = f_name + s_tag + '.html'
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # f = open(filename+s_tag+'.txt', 'w')  # 'words/python/'+link[7:12]+'/'
        content_tags = soup.find_all(s_tag)
        # filename = "info/" + str(c) + "/" + s_tag + ".txt"
        c += 1
        with open(filename, "w") as f:
            for c_tag in content_tags:
                sub_content_scrapper(c_tag, f)
                # for c in content:
                #     while c
                # cntnt = str(str(c_tag.contents).encode('utf-8')) + '\n'  # .replace("b'", '')
                # f.write(cntnt.replace(cntnt[-1], ''))


j = 0
for link in links:
    print(links.index(link), link)
    main_content_scrapper(link, j)
    j += 1

print("--- %s seconds ---" % (time.time() - start_time))
