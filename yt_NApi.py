import urllib
# import urllib.request  # url processing
from flask import Flask, request, render_template  # flask importing
import re  # regular expression ie searching a string in collection of data
from urllib.request import urlopen
import json
import requests
from urllib.error import HTTPError


app = Flask(__name__)

title = []
video_ids = []
like_count = []
dislike_count = []
view_count = []


def process(keyword):
    # print("search keyword : ", search_keyword)
    full_data = {}
    try:
        skill_set.append(keyword)
        html = urlopen(
            "https://www.youtube.com/results?search_query=" + keyword.replace(" ", ""))  # searching in youtube
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # collecting video ids from youtube
        title = []  # title list declaration for storing youtube video titles
        for VideoID in video_ids:
            if video_ids.index(VideoID) == 2:
                continue
            # print(
            #     "####################################################################################################################################\n\n")
            params = {"url": "https://www.youtube.com/watch?v=" + VideoID, "format": "json"}
            url = "https://www.youtube.com/oembed"
            query_string = urllib.parse.urlencode(params)
            query_string = query_string.replace('https%3A%2F%2F', 'http://')
            url = url + "?" + query_string
            print(url)

            with urllib.request.urlopen(url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                title.append(data['title'])
    except:
        pass
    finally:
        video_ids = video_ids[:5]
        # full_data.append(title[:10])
        # --------------------list declaretions-------------------------------------w
        v_id = []
        view_count = []
        like_count = []
        dislike_count = []
        for id in video_ids:
            url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&t&key=AIzaSyAvp49alnVMEPxu-DVV1j8SSkowIrtLCjQ' % id
            response = urlopen(url)
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')  # JSON default
            data = json.loads(raw_data.decode(encoding))
            items = data['items']
            v_id.append(items[0]['id'])
            statistics = items[0]['statistics']
            view_count.append(statistics['viewCount'])
            like_count.append(statistics['likeCount'])
            dislike_count.append(statistics['dislikeCount'])
        full_data.update({"title": title})
        full_data.update({"v_id": v_id})
        full_data.update({"view_count": view_count})
        full_data.update({"like_count": like_count})
        full_data.update({"dislike_count": dislike_count})
    return full_data


# home url routing
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', full_data=[])


# s = requests.Session()
#
# s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('http://httpbin.org/cookies')

# url routing when button clicking
@app.route('/', methods=['POST'])
def my_form_post():
    search_keyword = request.form['text']
    global skill_set
    skill_set = []
    complt_data = []
    if search_keyword.lower() == 'web development':
        f = open('skill/web development.txt', 'r')
        # g = open('skill/op.txt', 'w')
        for skill in f:
            f_data = process(skill)
            f_data.update({'skill': skill.upper()})
            complt_data.append(f_data)
        print(complt_data)
        print(len(complt_data))
        print(len(complt_data[0]))
    else:
        f_data = process(search_keyword)
        f_data.update({'skill': search_keyword.upper()})
        complt_data.append(f_data)
        print(complt_data)
        print(len(complt_data))
        print(len(complt_data[0]))

    # return  render_template('index.html')
    return render_template('show1.html', search_keyword=search_keyword.title(), complt_data=complt_data,
                           data_count=len(complt_data))


app.run(debug=True)
