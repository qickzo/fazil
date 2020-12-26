import urllib
from pprint import pprint
# import urllib.request  # url processing
from flask import Flask, request, render_template  # flask importing
import re  # regular expression ie searching a string in collection of data
from urllib.request import urlopen
import json
# import requests
from urllib.error import HTTPError
# import threading
# import concurrent.futures

app = Flask(__name__)

allowed_categid = [27, 28]
# non_list_channel = [
#     'UC1tVU8H153ZFO9eRsxdJlhA',
#     'UCeVMnSShP_Iviwkknt83cww',
#     'UC0LICD-FJ2FuA3FQ3ZiiLtw',
#     'UCl1Umy9WXb3I49JTMG3WoWw',
#     #'UCNT5YLfnn2cQGIxGw8iOxJQ'
# ]
courses = ['web development', 'app development']


def process(keyword):
    black_list = set()
    f_data = {}
    global title
    title = []  #1
    channel_id = []  #2
    v_id = []  #3
    lang_check = []
    global video_ids
    video_ids = []  #4
    view_count = []  #5
    like_count = []  #6
    dislike_count = []  #7
    full_data = {}
    global rm_vid
    rm_vid = []
    rm_categ_id = []
    categ_id = []  #8
    urllst = [] #9
    lang = []
    try:

        # skill_set.append(keyword)
        html = urlopen(
            "https://www.youtube.com/results?search_query={}&sp=EgIYAg%253D%253D".format(keyword.replace(" ", "")))# searching in youtube

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # collecting video ids from youtube
        video_ids = list(dict.fromkeys(video_ids))

    except urllib.error.HTTPError:
        pass
    finally:
        i = 0
        for id in video_ids:
            sngl_vdo_dtl = {}
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=contentDetails&id=%s&t&key=AIzaSyAvp49alnVMEPxu-DVV1j8SSkowIrtLCjQ' % id
            print(i)  ###################################################
            i += 1      ###################################################
            print(url)  ###################################################
            urllst.append(url)
            sngl_vdo_dtl.update({'url': url})
            response = urlopen(url)
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')  # JSON default
            data = json.loads(raw_data.decode(encoding))
            items = data['items']
            # v_id.append(items[0]['id'])
            sngl_vdo_dtl.update({'v_id': id})
            print(items[0]['id'])   ###################################################
            # channel_id.append(items[0]['snippet']['channelId'])
            sngl_vdo_dtl.update({'chnlid': items[0]['snippet']['channelId']})
            print(items[0]['snippet']['channelId'])     ###################################################
            statistics = items[0]['statistics']
            # categ_id.append(int(items[0]['snippet']['categoryId']))
            sngl_vdo_dtl.update({'cid': int(items[0]['snippet']['categoryId'])})
            print('category : ', int(items[0]['snippet']['categoryId']))   ###################################################
            if int(items[0]['snippet']['categoryId']) not in allowed_categid:
                rm_categ_id.append(int(items[0]['snippet']['categoryId']))
            # title.append(items[0]['snippet']['title'])
            sngl_vdo_dtl.update({"title": items[0]['snippet']['title']})
            print(items[0]['snippet']['title'])
            t = items[0]['snippet']['title']
            # desc = items[0]['snippet']['description']

            # if 'hindi' in t.lower():
            #     rm_vid.append(id)
            # restrctkeywd = 'hindi|malayalam|urdu|bengali|telugu|tamil|gujarati|kannada|punjabi|marathi'
            # if re.findall(restrctkeywd, t.lower()) or re.findall(restrctkeywd, desc.lower()):
            #     rm_vid.append(id)
            try:
                # view_count.append(statistics['viewCount'])
                sngl_vdo_dtl.update({'view_count': statistics['viewCount']})
            except:
                # view_count.append(None)
                sngl_vdo_dtl.update({'view_count': 'None'})
            try:
                # like_count.append(statistics['likeCount'])
                sngl_vdo_dtl.update({'like_count': statistics['likeCount']})
            except:
                # like_count.append(None)
                sngl_vdo_dtl.update({'like_count': 'None'})
            try:
                # dislike_count.append(statistics['dislikeCount'])
                sngl_vdo_dtl.update({'dislike_count': statistics['dislikeCount']})
            except:

                # dislike_count.append(None)
                sngl_vdo_dtl.update({'dislike_count': 'None'})
            try:
                # lang_check.append([items[0]['snippet']['defaultAudioLanguage'],'title : '+t])
                # lang.append(items[0]['snippet']['defaultAudioLanguage'])
                sngl_vdo_dtl.update({'lang': items[0]['snippet']['defaultAudioLanguage']})
                # if 'en' not in  items[0]['snippet']['defaultAudioLanguage']:
                #     rm_vid.append(id)
            except:
                lang_check.append(['none', 'title : '+t])
                # lang.append('none')
                sngl_vdo_dtl.update({'lang': 'None'})
            full_data.update({id: sngl_vdo_dtl})

        print('---------------------len---', len(full_data))
        for itm in full_data:
            if 'en' not in full_data[itm]['lang']:
                black_list.add(itm)
            if full_data[itm]['cid'] not in allowed_categid:
                black_list.add(itm)

        for i in black_list:
            del full_data[i]
        print('---------------------len---', len(full_data))
        count = 0
        for item in full_data:
            if count < 5:
                f_data.update({item: full_data[item]})
                count += 1
        print('lllllllllllllllllllllllllllllllllll len = ', len(f_data.keys()))
            # print(
            #     '############################# in loop ############################################################################')
            # print(title)
            # print(v_id)
            # print(like_count)
            # print(dislike_count)
            # print(urllst)
            # print(categ_id)
            # print(lang)
        # print('#############################FIRST############################################################################')
        # print(len(title))
        # print(len(video_ids))
        # print(len(like_count))
        # print(len(dislike_count))
        # print(len(urllst))
        # print(len(lang))




        # print(
        #     '#######################SECOND##################################################################################')
        # print(len(title))
        # print(len(video_ids))
        # print(len(like_count))
        # print(len(dislike_count))
        # print(len(urllst))
        # print(len(lang))

        
        # for chnl in non_list_channel:
        #     while chnl in channel_id:
        #         print('************** non list channel before***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)
        #
        #         cidx = channel_id.index(chnl)
        #         categ_id.remove(categ_id[cidx])
        #         channel_id.remove(channel_id[cidx])
        #         v_id.remove(v_id[cidx])
        #         video_ids.remove(video_ids[cidx])
        #         view_count.remove(view_count[cidx])
        #         title.remove(title[cidx])
        #         like_count.remove(like_count[cidx])
        #         dislike_count.remove(dislike_count[cidx])
        #         urllst.remove(urllst[cidx])
        #         lang.remove(lang[cidx])
        #
        #         print('************** non list channel after***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)

        # print(
        #     '####################THIRD#####################################################################################')
        # print(len(title))
        # print(len(video_ids))
        # print(len(like_count))
        # print(len(dislike_count))
        # print(len(urllst))
        # print(len(lang))

        # for cid in rm_categ_id:
        #     while cid in categ_id:
                # print('************** rm categ id before ***********************')
                # print(title)
                # print(v_id)
                # print(like_count)
                # print(dislike_count)
                # print(urllst)
                # print(categ_id)
                # print(lang)

                # print(len(title))
                # print(len(video_ids))
                # print(len(like_count))
                # print(len(dislike_count))
                # print(len(urllst))
                # print(len(lang))

                # catidx = categ_id.index(cid)
                # categ_id.remove(categ_id[catidx])
                # v_id.remove(v_id[catidx])
                # video_ids.remove(video_ids[catidx])
                # title.remove(title[catidx])
                # view_count.remove(view_count[catidx])
                # channel_id.remove(channel_id[catidx])
                # like_count.remove(like_count[catidx])
                # dislike_count.remove(dislike_count[catidx])
                # urllst.remove(urllst[catidx])
                # lang.remove(lang[catidx])

                # print('************** rm categ id after ***********************')
                # print(title)
                # print(v_id)
                # print(like_count)
                # print(dislike_count)
                # print(urllst)
                # print(categ_id)
                # print(lang)

                # print(len(title))
                # print(len(video_ids))
                # print(len(like_count))
                # print(len(dislike_count))
                # print(len(urllst))
                # print(len(lang))


        # print('###################FOURTH######################################################################################')
        # print(len(title))
        # print(len(video_ids))
        # print(len(like_count))
        # print(len(dislike_count))
        # print(len(urllst))
        # print(len(lang))

        # for lg in lang:
        #     if 'en' not in lg:
        #         print('************** lang before***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)
        #
        #         lidx = lang.index(lg)
        #         categ_id.remove(categ_id[lidx])
        #         v_id.remove(v_id[lidx])
        #         video_ids.remove(video_ids[lidx])
        #         title.remove(title[lidx])
        #         view_count.remove(view_count[lidx])
        #         channel_id.remove(channel_id[lidx])
        #         like_count.remove(like_count[lidx])
        #         dislike_count.remove(dislike_count[lidx])
        #         urllst.remove(urllst[lidx])
        #         lang.remove(lang[lidx])
        #
        #         print('************** lang after***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)

        # for item in rm_vid:
        #     if item in video_ids:
        #         print('************** rm vid before***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)
        #
        #         print('item  : ', item)
        #         idx = v_id.index(item)
        #         print('idx : ', idx)
        #         print('channel_id[idx] : ', channel_id[idx])
        #         channel_id.remove(channel_id[idx])
        #         print("v_id[idx] : ", v_id[idx])
        #         v_id.remove(v_id[idx])
        #         print('categ_id[idx] : ', categ_id[idx])
        #         categ_id.remove(categ_id[idx])
        #         print('video_ids[idx] : ', video_ids[idx])
        #         video_ids.remove(video_ids[idx])
        #         print('view_count[idx] : ', view_count[idx])
        #         view_count.remove(view_count[idx])
        #         print('title[idx] : ', title[idx])
        #         title.remove(title[idx])
        #         print('like_count[idx] : ', like_count[idx])
        #         like_count.remove(like_count[idx])
        #         print('dislike_count[idx] : ', dislike_count[idx])
        #         dislike_count.remove(dislike_count[idx])
        #         print('urllst[idx] : ', urllst[idx])
        #         urllst.remove(urllst[idx])
        #         print('lang[idx] : ', lang[idx])
        #         lang.remove(lang[idx])
        #
        #         print('************** rm vid after***********************')
        #         print(title)
        #         print(v_id)
        #         print(like_count)
        #         print(dislike_count)
        #         print(urllst)
        #         print(categ_id)
        #         print(lang)

        # print(
        #     '################### FIFTH ######################################################################################')
        # print(len(title))
        # print(len(video_ids))
        # print(len(like_count))
        # print(len(dislike_count))
        # print(len(urllst))
        # print(len(lang))
        # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$\n', lang, '\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #
        # print(title)
        # print(v_id)
        # print(like_count)
        # print(dislike_count)
        # print(urllst)
        # print(categ_id)
        # print(lang)

        # full_data.update({"title": title})
        # full_data.update({"v_id": v_id})
        # full_data.update({"cid": categ_id})
        # full_data.update({"view_count": view_count})
        # full_data.update({"like_count": like_count})
        # full_data.update({"dislike_count": dislike_count})
        # full_data.update({'url': urllst})
        # if len(v_id) < 5:
        #     full_data.update({'size': len(v_id)})
        # else:
        #     full_data.update({'size': 5})
        # pprint(full_data)
        for i in f_data:
            print(f_data[i]['lang'])
        print('\n\n')
        for i in f_data:
            print(f_data[i]['cid'])
    return f_data


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    search_keyword = request.form['text']
    global skill_set
    skill_set = []
    complt_data = []
    if search_keyword.lower() in courses:
        f = open('skill/{}.txt'.format(search_keyword.lower()), 'r')
        for skill in f:
            print('************************{}*************************'.format(skill.replace('\n', '')))
            f_data = process(skill.replace('\n', ''))
            f_data.update({'skill': skill.upper()})
            complt_data.append(f_data)
    else:
        f_data = process(search_keyword)
        # if len(f_data) > 5:
        #     f_data.update({'size': 5})
        # else:
        #     f_data.update({'size':len(f_data)})
        f_data.update({'skill': search_keyword.upper()})
        complt_data.append(f_data)
        pprint(complt_data)
        for j in complt_data[0]:
            print(j)
    # return render_template('index.html')
    return render_template('show1.html', search_keyword=search_keyword.title(), complt_data=complt_data,
                           data_count=len(complt_data))


if __name__ == '__main__':
    app.run(debug=True)

