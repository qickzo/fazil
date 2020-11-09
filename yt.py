# import urllib.request
# import json
# import urllib
#
#
# #change to yours VideoID or change url inparams
# VideoID = "SZj6rAYkYOg"
#
# params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
# url = "https://www.youtube.com/oembed"
# query_string = urllib.parse.urlencode(params)
# url = url + "?" + query_string
#
# with urllib.request.urlopen(url) as response:
#     response_text = response.read()
#     data = json.loads(response_text.decode())
#     # pprint.pprint(data)
#     print(data['title'])
#
# # import requests
# # from bs4 import BeautifulSoup
#
# # base_url ='https://www.youtube.com/watch?'
# # search_string = 'v=lMvKVZWwGRo'
# # url = base_url + search_string
# # print(url)
# # supers=requests.get(url).content
# # print(supers)
# # data = BeautifulSoup(supers,'html.parser')
# # print(data)
# # videos =data.find_all('a', class_= 'content-link spf-link yt-uix-sessionlink spf-link')
# # print(videos)
# # for video in videos:
# #     print(video.find('span', class_='title').get_text())


# num = [[1,2,3], [4,5,6]]
# print(num[0])
#
# print(num[0][i])

from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs # importing BeautifulSoup

# sample youtube video url
video_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
# init an HTML Session
session = HTMLSession()
# get the html content
response = session.get(video_url)
# execute Java-script
response.html.render(sleep=1)
# create bs object to parse HTML
soup = bs(response.html.html, "html.parser")
# write all HTML code into a file
open("video.html", "w", encoding='utf8').write(response.html.html)