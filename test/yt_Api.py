# Import modules
# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
# import pandas as pd
# import pprint
# import matplotlib.pyplot as plt

from flask import Flask,  request, render_template  # flask importing

# Set up YouTube credentials
DEVELOPER_KEY = 'AIzaSyBvVApxxBXKOztbGJvKINYNywl0UsCXTbI'

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

app = Flask(__name__)


# home url routing
@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', full_data=[])


youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


def youtubeSearch(query, max_results=1, order="relevance", token=None, location=None, location_radius=None):
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=max_results,
        location=location,
        locationRadius=location_radius).execute()

    items = search_response['items']  # 50 "items"

    # Assign 1st results to title, channelId, datePublished then print
    title = items[0]['snippet']['title']
    channelId = items[0]['snippet']['channelId']
    datePublished = items[0]['snippet']['publishedAt']

    return search_response


def storeResults(response):
    # create variables to store your values
    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []

    for search_result in response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            # append title and video for each item
            title.append(search_result['snippet']['title'])
            videoId.append(search_result['id']['videoId'])

            # then collect stats on each video using videoId
            stats = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(stats['items'][0]['snippet']['channelId'])
            channelTitle.append(stats['items'][0]['snippet']['channelTitle'])
            categoryId.append(stats['items'][0]['snippet']['categoryId'])
            favoriteCount.append(stats['items'][0]['statistics']['favoriteCount'])
            viewCount.append(stats['items'][0]['statistics']['viewCount'])

            # Not every video has likes/dislikes enabled so they won't appear in JSON response
            try:
                likeCount.append(stats['items'][0]['statistics']['likeCount'])
            except:
                # Good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Likes Count is not available".format(
                    stats['items'][0]['snippet']['title'],
                    stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                # Appends "Not Available" to keep dictionary values aligned
                likeCount.append("Not available")

            try:
                dislikeCount.append(stats['items'][0]['statistics']['dislikeCount'])
            except:
                # Good to be aware of Channels that turn off their Likes
                print("Video titled {0}, on Channel {1} Dislikes Count is not available".format(
                    stats['items'][0]['snippet']['title'],
                    stats['items'][0]['snippet']['channelTitle']))
                print(stats['items'][0]['statistics'].keys())
                dislikeCount.append("Not available")

            # Sometimes comments are disabled so if they exist append, if not append nothing...
            # It's not uncommon to disable comments, so no need to wrap in try and except
            if 'commentCount' in stats['items'][0]['statistics'].keys():
                commentCount.append(stats['items'][0]['statistics']['commentCount'])
            else:
                commentCount.append(0)

            if 'tags' in stats['items'][0]['snippet'].keys():
                tags.append(stats['items'][0]['snippet']['tags'])
            else:
                # I'm not a fan of empty fields
                tags.append("No Tags")

    # Break out of for-loop and if statement and store lists of values in dictionary
    youtube_dict = {'tags': tags, 'channelId': channelId, 'channelTitle': channelTitle,
                    'categoryId': categoryId, 'title': title, 'videoId': videoId,
                    'viewCount': viewCount, 'likeCount': likeCount, 'dislikeCount': dislikeCount,
                    'commentCount': commentCount, 'favoriteCount': favoriteCount}

    return youtube_dict


global results


@app.route('/', methods=['POST'])
def my_form_post():
    global results
    skill_set = []
    full_data = []
    title = []
    like = []
    views = []
    dislike = []
    video = []
    search_keyword = request.form['text']  # searching keyword collect from text box
    if search_keyword.lower() == 'web development':
        f = open('skill/web development.txt', 'r')
        # g = open('skill/op.txt', 'w')
        for skill in f:
            skill_set.append(skill)
            response = youtubeSearch(skill)
            results = storeResults(response)
            title.append(results['title'])
            views.append(results['viewCount'])
            like.append(results['likeCount'])
            dislike.append(results['dislikeCount'])
            video.append(results['videoId'])
            print(title)
            print(views)
            print(like)
            print(dislike)
            print(video)

    else:
        print('search keyword : ', search_keyword)
        skill_set.append(search_keyword)
        response = youtubeSearch(search_keyword)
        results = storeResults(response)
        title.append(results['title'])
        print(title)
        views.append(results['viewCount'])
        print(views)
        like.append(results['likeCount'])
        print(like)
        dislike.append(results['dislikeCount'])
        print(dislike)
        video.append(results['videoId'])
        print(video)

    return render_template('show.html', search_keyword=search_keyword.title(), skill_set=skill_set,
                           title=title, like=like, dislike=dislike, views=views, video=video, n=len(skill_set))


if __name__ == '__main__':
    app.run(debug=True)


