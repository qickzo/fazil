import urllib
import os
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session
import re
from urllib.request import urlopen
import json
from json import load
from urllib.error import HTTPError
import pymongo
import bcrypt
import pyotp
from flask_mail import Message, Mail

app = Flask(__name__)
app.secret_key = "testing"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dhackz101@gmail.com'
app.config['MAIL_PASSWORD'] = 'mukxgmrdiggumwev'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

client = pymongo.MongoClient()
db = client.get_database('User_accounts')
records = db.register




@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


allowed_categid = [27, 28]
courses = ['web development', 'app development']


@app.route('/delete/<course_name>')
def delete(course_name):
    email = session['email']
    userfound = records.find_one({'email': email})
    course = userfound['course']
    for sk in course:
        if sk['skill'] == course_name:
            index = course.index(sk)
            course.remove(course[index])
    records.update_one({'email': email}, {"$set": {'course': course}})
    return redirect(url_for("logged_in"))


@app.route('/course/<course_name>')
def course(course_name):
    email = session['email']
    userfound = records.find_one({'email': email})
    course = userfound['course']
    for sk in course:
        if sk['skill'] == course_name: c_data =  sk['skill_data']

    return render_template('course.html', search_keyword=course_name.title(), complt_data=c_data,
                           data_count=len(c_data), course_name=course_name )
@app.route('/validate', methods=['POST'])
def validate():
    d1, d2, d3, d4, d5, d6 = request.form.get('d1'), request.form.get('d2'), request.form.get('d3'), request.form.get('d4'),request.form.get('d5'),request.form.get('d6')
    otp = int(session['otp'])
    print('otp : ', type(otp))
    otpp = int(d1+d2+d3+d4+d5+d6)
    print('otpp : ', type(otpp))
    if otp == otpp:
        return render_template('change_password.html')
    else:
        return render_template('otp_request.html')


@app.route('/change_password', methods=['POST'])
def change_password():
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email_found = records.find_one({'email':email})
        if password1 != password2:
            message = 'Passwords should  match!'
            return render_template('change_password.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

            email_found['password'] = hashed

            records.save(email_found)
            return render_template('course.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == "POST":
        email = request.form.get("email")
        email_found = records.find_one({'email': email})
        if email_found:
            totp = pyotp.TOTP('base32secret3232')
            otp = totp.now()
            session['otp'] = otp
            msg = Message(subject='otp', body=str(otp), sender='dhackz101@gmail.com', recipients=[email])
            mail.send(msg)
            return render_template('otp_request.html')
        return redirect(url_for("reset_password_request"))
    return render_template('reset_password_request.html')


@app.route("/sign_up", methods=['post', 'get'])
def sign_up():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('signup.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)
        if password1 != password2:
            message = 'Passwords should  match!'
            return render_template('signup.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed, 'course': []}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            new_name = user_data['name']
            session["email"] = new_email
            session["name"] = new_name

            return redirect(url_for('logged_in'))

    return render_template('signup.html')


@app.route('/courses')
def logged_in():
    if "email" in session:
        email = session["email"]
        name = session["name"]
        authenticated = True
        course = records.find_one({'email': email})['course']
        print(type(course))
        # return render_template('profile.html', name=name.title(), email=email, authenticated=authenticated)
        return render_template('dashboard.html', course=course)
    else:
        return redirect(url_for("sign_in"))


@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            name_val = email_found['name']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                session["name"] = name_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('signin.html', message=message)
        else:
            message = 'Email not found'
            return render_template('signin.html', message=message)
    return render_template('signin.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("index.html")
    else:
        return  redirect(url_for("sign_in"))


@app.route('/enrol')
@app.route('/enroll')
def enroll():
    if "email" in session:
        email = session['email']
        complt_data = session['course']
        skill = session['skill']
        userfound = records.find_one({'email': email})
        course = userfound['course']
        print("first:\n\n")
        pprint({"course": course})
        course.append({'skill': skill, 'skill_data': complt_data})
        print("second:\n\n")
        pprint({"course": course})

        records.update_one({'email': email}, {"$set": {'course': course}})
        userfound = records.find_one({'email': email})
        print("last:\n\n")
        pprint({"course": userfound['course']})
        # return render_template('')
    return redirect(url_for('sign_in'))


def process(keyword):
    black_list = set()
    f_data = {}
    video_ids = []
    full_data = {}
    rm_categ_id = []
    try:
        html = urlopen(
            "https://www.youtube.com/results?search_query={}&sp=EgIYAg%253D%253D".format(keyword.replace(" ", "")))

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids = list(dict.fromkeys(video_ids))

    except urllib.error.HTTPError:
        pass
    finally:
        i = 0
        for id in video_ids:
            sngl_vdo_dtl = {}
            url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet&part=statistics&part=contentDetails&id=%s&t&key=AIzaSyAvp49alnVMEPxu-DVV1j8SSkowIrtLCjQ' % id
            print(i)
            i += 1
            print(url)
            sngl_vdo_dtl.update({'url': url})
            response = urlopen(url)
            raw_data = response.read()
            encoding = response.info().get_content_charset('utf8')  # JSON default
            data = json.loads(raw_data.decode(encoding))
            items = data['items']
            sngl_vdo_dtl.update({'v_id': id})
            print(items[0]['id'])
            sngl_vdo_dtl.update({'chnlid': items[0]['snippet']['channelId']})
            print(items[0]['snippet']['channelId'])
            statistics = items[0]['statistics']
            sngl_vdo_dtl.update({'cid': int(items[0]['snippet']['categoryId'])})
            print('category : ', int(items[0]['snippet']['categoryId']))
            if int(items[0]['snippet']['categoryId']) not in allowed_categid:
                rm_categ_id.append(int(items[0]['snippet']['categoryId']))
            sngl_vdo_dtl.update({"title": items[0]['snippet']['title']})
            print(items[0]['snippet']['title'])

            try:
                sngl_vdo_dtl.update({'view_count': statistics['viewCount']})
            except:
                sngl_vdo_dtl.update({'view_count': 'None'})
            try:
                sngl_vdo_dtl.update({'like_count': statistics['likeCount']})
            except:
                sngl_vdo_dtl.update({'like_count': 'None'})
            try:
                sngl_vdo_dtl.update({'dislike_count': statistics['dislikeCount']})
            except:
                sngl_vdo_dtl.update({'dislike_count': 'None'})
            try:
                sngl_vdo_dtl.update({'lang': items[0]['snippet']['defaultAudioLanguage']})
            except:
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

        for i in f_data:
            print(f_data[i]['lang'])
        print('\n\n')
        for i in f_data:
            print(f_data[i]['cid'])
    return f_data


@app.route('/', methods=['GET'])
@app.route('/index ', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    search_keyword = request.form['text']
    session['skill'] = search_keyword.title()
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
                    f_data = process(sub_skill)  # .replace('\n', ''))
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
        pprint(complt_data)

        for j in complt_data[0]:
            print(j)
    # return render_template('index.html')
    flag = True
    if "email" in session:
        flag = None
    session['course'] = complt_data
    return render_template('shw.html', search_keyword=search_keyword.title(), complt_data=complt_data,
                           data_count=len(complt_data), flag=flag)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

