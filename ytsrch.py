from flask import Flask,  request, render_template  # flask importing
from markupsafe import escape

import urllib.request  # url processing
import re  # regular expression ie searching a string in collection of data


import json
import urllib

app = Flask(__name__)


# home url routing
@app.route('/', methods=['GET'])
def hello_world():
	return render_template('index.html', full_data=[])


# url routing when button clicking
@app.route('/', methods=['POST'])
def my_form_post():
	full_data = []
	search_keyword = request.form['text'] # searching keyword collect from text box
	print("search keyword : ", search_keyword)
	html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword.replace(" ", "+"))  #searching in youtube
	video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # collecting video ids from youtube
	title = []  # title list declaration for storing youtube video titles
	for VideoID in video_ids:
		print("####################################################################################################################################\n\n")
		params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
		print("params = ", params)
		url = "https://www.youtube.com/oembed"
		query_string = urllib.parse.urlencode(params)
		print("query string : ", query_string)
		url = url + "?" + query_string
		print("url : ", url)

		with urllib.request.urlopen(url) as response:
			response_text = response.read()
			data = json.loads(response_text.decode())
			print("data : ", data)
			title.append(data['title'])
			print("title : ", title)
	full_data.append(title[:10])
	full_data.append(video_ids[:10])
	print("full_data : ", full_data)
	print("length of full data : ", len(full_data),"len(full_data[0]), len(full_data[1]) : ", len(full_data[0]),len(full_data[0]))
	return render_template('show.html', search_keyword=search_keyword.title(), full_data=full_data)
	# search_keyword.title() used for convert searching keyword into title format


if __name__ == '__main__':
	app.run(debug=True)

