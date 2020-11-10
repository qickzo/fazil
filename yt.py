from bs4 import BeautifulSoup
import requests
url = "https://www.youtube.com/watch?v=mU6anWqZJcc&t=445s"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
# print(soup.title.string)
# print(soup.find_all('span'))
# for link in soup.find_all('yt-view-count-renderer'):
#     print('#####################################################################################################')
#     print(link.text)
tag = soup.html
tag.name = "span"
# print(tag.find_all(id='info-text'))
f = open('yt.html', 'a')
# for i in range(3):
a =  soup.find("div", {"id": "count"})
chi = a.contents
print(a)
f.write(str(chi))
f.close()
