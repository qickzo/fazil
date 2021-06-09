from yt_NApi import process, courses
from flask import Flask, render_template, request
from json import load

test = Flask(__name__)


@test.route('/', methods=['GET'])
@test.route('/index ', methods=['GET'])
def hello_world():
    return render_template('index.html')


@test.route('/', methods=['POST'])
def my_form_post():
    # data = {}
    # f = open('skill/web development.json')
    # f = load(f)
    # for line in f["topic"]:
    #     data[line]
    # return 'hello'
    search_keyword = request.form['text']
    global skill_set
    skill_set = []
    complt_data = []
    if search_keyword.lower() in courses:
        f = open('skill/{}.json'.format(search_keyword.lower()), 'r')
        f = load(f)
        for skill in f['topic']:
            if type(skill) == type(list()):
                sub_data = {}
                sub_data.update({'nested': True})
                videos = []
                for sub_skill in skill:
                    print('************************{}*************************'.format(sub_skill))
                    f_data = process(sub_skill)#.replace('\n', ''))
                    f_data.update({'skill': sub_skill.upper()})
                    if skill.index(sub_skill) == 0:
                        sub_data.update({'skill': sub_skill})
                    # else:
                    #     f_data.update({'title': False, 'choice': True})
                    videos.append(f_data)
                sub_data.update({'videos': videos, 'count': len(videos)})
                complt_data.append(sub_data)
            else:
                print('************************{}*************************'.format(skill.replace('\n', '')))
                f_data = process(skill)
                f_data.update({'skill': skill.upper(), 'nested': False})
                complt_data.append(f_data)

    else:
        f_data = process(search_keyword)
        f_data.update({'skill': search_keyword.upper()})
        complt_data.append(f_data)
        # pprint(complt_data)
        for j in complt_data[0]:
            print(j)
    # return render_template('index.html')
    flag = True
    # if "email" in session:
    #     flag = None

    return render_template('shw.html', search_keyword=search_keyword.title(), complt_data=complt_data,
                           data_count=len(complt_data))


if __name__ == '__main__':
    test.run(debug=True, port=5002)
