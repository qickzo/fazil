import urllib
# import urllib.request  # url processing
from flask import Flask, request, render_template  # flask importing
import re  # regular expression ie searching a string in collection of data
from urllib.request import urlopen
import json
import requests
from urllib.error import HTTPError

app = Flask(__name__)

allowed_categid = [22, 27, 28]
non_list_channel = ['UC1tVU8H153ZFO9eRsxdJlhA', 'UCeVMnSShP_Iviwkknt83cww', 'UC0LICD-FJ2FuA3FQ3ZiiLtw','UCl1Umy9WXb3I49JTMG3WoWw']


def process(keyword):
    global title
    title = []
    channel_id = []
    v_id = []
    global video_ids
    video_ids = []
    view_count = []
    like_count = []
    dislike_count = []
    full_data = {}
    global rm_vid
    rm_vid = []
    rm_categ_id = []
    categ_id = []
    try:

        skill_set.append(keyword)
        html = urlopen(
            "https://www.youtube.com/results?search_query={}&sp=EgIYAg%253D%253D".format(keyword.replace(" ", "")))# searching in youtube

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # collecting video ids from youtube
        video_ids = list(dict.fromkeys(video_ids))

    except urllib.error.HTTPError:
        pass
    finally:

        for id in video_ids:
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=contentDetails&id=%s&t&key=AIzaSyAvp49alnVMEPxu-DVV1j8SSkowIrtLCjQ' % id
            # print(url)
            response = urlopen(url)
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')  # JSON default
            data = json.loads(raw_data.decode(encoding))
            items = data['items']
            v_id.append(items[0]['id'])
            channel_id.append(items[0]['snippet']['channelId'])
            statistics = items[0]['statistics']
            categ_id.append(int(items[0]['snippet']['categoryId']))
            if int(items[0]['snippet']['categoryId']) not in allowed_categid:
                rm_categ_id.append(int(items[0]['snippet']['categoryId']))
            title.append(items[0]['snippet']['title'])
            t = items[0]['snippet']['title']
            desc = items[0]['snippet']['description']

            if 'hindi' in t.lower() :
                rm_vid.append(id)
            restrctkeywd = 'hindi|malayalam|urdu|bengali|telugu|tamil|gujarati|kannada|punjabi|marathi'
            if re.findall(restrctkeywd, t.lower()) or re.findall(restrctkeywd, desc.lower()):
                rm_vid.append(id)
            view_count.append(statistics['viewCount'])
            like_count.append(statistics['likeCount'])
            dislike_count.append(statistics['dislikeCount'])
        print('#########################################################################################################')
        print(len(title))
        print(len(video_ids))
        print(len(like_count))
        print(len(dislike_count))

        for item in rm_vid:
            if item in video_ids:
                idx = video_ids.index(item)
                channel_id.remove(channel_id[idx])
                v_id.remove(v_id[idx])
                categ_id.remove(categ_id[idx])
                video_ids.remove(video_ids[idx])
                title.remove(title[idx])
                like_count.remove(like_count[idx])
                dislike_count.remove(dislike_count[idx])
        print(
            '#########################################################################################################')
        print(len(title))
        print(len(video_ids))
        print(len(like_count))
        print(len(dislike_count))

        for chnl in non_list_channel:
            while chnl in channel_id:
                cidx = channel_id.index(chnl)
                categ_id.remove(categ_id[cidx])
                channel_id.remove(channel_id[cidx])
                v_id.remove(v_id[cidx])
                video_ids.remove(video_ids[cidx])
                title.remove(title[cidx])
                like_count.remove(like_count[cidx])
                dislike_count.remove(dislike_count[cidx])

        print(
            '#########################################################################################################')
        print(len(title))
        print(len(video_ids))
        print(len(like_count))
        print(len(dislike_count))

        for cid in rm_categ_id:
            while cid in categ_id:
                catidx = categ_id.index(cid)
                categ_id.remove(categ_id[catidx])
                v_id.remove(v_id[catidx])
                video_ids.remove(video_ids[catidx])
                title.remove(title[catidx])
                like_count.remove(like_count[catidx])
                dislike_count.remove(dislike_count[catidx])

        print(
            '#########################################################################################################')
        print(len(title))
        print(len(video_ids))
        print(len(like_count))
        print(len(dislike_count))

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


# url routing when button clicking
@app.route('/', methods=['POST'])
def my_form_post():
    search_keyword = request.form['text']
    global skill_set
    skill_set = []
    complt_data = []
    if search_keyword.lower() == 'web development':
        f = open('skill/web development.txt', 'r')
        for skill in f:
            f_data = process(skill.replace('\n', ''))
            f_data.update({'skill': skill.upper()})
            complt_data.append(f_data)
    else:
        f_data = process(search_keyword)
        f_data.update({'skill': search_keyword.upper()})
        complt_data.append(f_data)
    # return  render_template('index.html')
    return render_template('show1.html', search_keyword=search_keyword.title(), complt_data=complt_data,
                           data_count=len(complt_data))


app.run(debug=True)
