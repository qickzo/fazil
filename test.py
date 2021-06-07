from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import errno
import requests
import io
import random
from collections import OrderedDict

i = 0
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

topics = ['route map for a python developer', 'python beginner to advanced topics']
for topic in topics:

    #                            google url scrapping
    # ----------------------------------------------------------------------------------
    with io.open('words/' + topic + '.html', 'w', encoding='utf8') as f:
        f.write('.......................................{}......................................'
                '..\n'.format(topic))
        print('.......................................{}......................................'
                '..\n'.format(topic))
        req = requests.get('https://www.google.com/search?q=' + topic.replace(' ', '+'), headers=headers_list[i]).text  # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64)'})# AppleWebKit /537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
        soup = BeautifulSoup(req, "html.parser")
        # f = open('w' + str(i) + '.html', 'w')
        links_a = soup.find_all('div', {'class': 'kCrYT'})  #

        # ----------------------------------------------------------------------------------

        links = []
        for link in links_a:
            try:
                # file = 'test2/wa{}.html'.format(c)
                # f = open(file, 'w')
                # c += 1
                cont = link.contents[0]['href']
                # print('-----1-------', cont)
                idx = cont.index('&sa=U&')
                cont = str(cont).replace(cont[idx:], '')
                cont = cont.replace('/url?q=', '')
                # print('-----2-------', cont)
                links.append(cont)
                # f.write(cont)
                # f.close()
            except:
                pass

        for link in links:
            print('link :::: ', link)

        c = 0
        for link in links:
            f.write('*********************************** {} ***************************************\n\n'.format(link))
            print('*********************************** {} ***************************************\n\n'.format(link))

            req = requests.get(link, headers=headers_list[i]).text#{'User-Agent': 'Mozilla/4.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
            i += 1
            if i == 4: i = 0
            # print(type(req))

            # page = urlopen(req).read()
            # page = link

            soup = BeautifulSoup(req, "html.parser")
            tags = ['strong', 'b', 'h1', 'h2', 'h3']
            for tag in tags:
                # filename = "words/" + link[12:14] + str(c) + "/" + tag + ".txt"
                #
                # if not os.path.exists(os.path.dirname(filename)):
                #     try:
                #         os.makedirs(os.path.dirname(filename))
                #     except OSError as exc:  # Guard against race condition
                #         if exc.errno != errno.EEXIST:
                #             raise
                # f = open('words/python/'+link[7:12]+'/'+tag+'.txt', 'w')
                words = soup.find_all(tag)
                # print('words ::::::::::     ', words)
                f.write('-----------------------------------{}--------------------------------------\n\n'.format(tag))
                print('-----------------------------------{}--------------------------------------\n\n'.format(tag))

                for word in words:
                    f.write(str(word))
                    f.write('\n===\n')
                    print(str(word))
                    print('\n===\n')

                # with open(filename, "w") as f:
                #     cntnt = str(str(word.contents).encode('utf-8')) + '\n'  # .replace("b'", '')
                #     f.write(cntnt.replace(cntnt[-1], ''))
                f.write(
                    '==========================================================================\n'.format(len(tag) * '+'))
                print(
                    '==========================================================================\n'.format(
                        len(tag) * '+'))
            f.write('***********************************{}***************************************\n\n'.format('+' * len(link)))
            print('***********************************{}***************************************\n\n'.format('+' * len(link)))
            # c += 1
        f.write('-------------completed---------------')
        print('-------------completed---------------')


