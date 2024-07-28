from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify,send_from_directory,send_file
from flask_mysqldb import MySQL
import bcrypt
import requests
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
import qrcode
from io import BytesIO
from func_timeout import func_set_timeout
import func_timeout

app = Flask(__name__)
app.secret_key = 'nyh314nyh'

# 配置 MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'huanyu'
app.config['MYSQL_PASSWORD'] = 'nyh314nyh'
app.config['MYSQL_DB'] = 'user_database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# scheduler = BackgroundScheduler()
# scheduler.start()


# @app.route('/add_job', methods=['POST'])
# def add_job():
#     job_data = request.json
#     job_id = job_data.get('job_id')
#     hour = job_data.get('hour')
#     minute = job_data.get('minute')
#     message = job_data.get('message')

#     # 动态添加一个任务到调度器
#     scheduler.add_job(
#         send_notification, 'cron', id=job_id, hour=hour, minute=minute,
#         args=[message]  # 将消息内容作为参数传给任务函数
#     )
#     return jsonify({"message": "Job added successfully!"}), 200

def send_notification(message):
    print(f"Notification: {message}")
    # 这里可以扩展为发送邮件、请求Web服务等操作
    

# 模拟的最新版本信息
latest_notifiy_info = {
    "title": "通知测试",
    "msg": "这是测试版本哦，有问题请反馈谢谢！",
    "time":"2024年6月28日"
}
@app.route('/get_msg', methods=['GET'])
def get_msg():
    
        return jsonify({"notifyId": "1", "notification": latest_notifiy_info})

# 模拟的最新版本信息
latest_version_info = {
    "version": "1.0.0",
    "url":  "https://www.212314.xyz/download/app-release.apk,https://www.wuthelper.top/download/app-release.apk",
    "release_notes": "修复一些小问题，完善了一下使用指南"
}
@app.route('/check_update', methods=['GET'])
def check_update():
    current_version = request.args.get('version')
    if current_version is None:
        return jsonify({"error": "Current version not specified"}), 400

    if current_version < latest_version_info['version']:
        return jsonify({"update": True, "latest_version_info": latest_version_info})
    else:
        return jsonify({"update": False, "message": "你已经是最新版了","latest_version_info": latest_version_info})
@func_set_timeout(3)  # 设定函数超执行时间_
# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.json
        username = userDetails['username']
        userid = userDetails['userid']
        password = userDetails['password'].encode('utf-8')
        email = userDetails['email']
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        
        # 检查用户名是否已存在
        result = cur.execute("SELECT * FROM user_accounts WHERE username = %s", [username])
        if result > 0:
            cur.close()
            return jsonify({'message': '用户名已存在'}), 400  # 用户名已存在，返回错误消息
        cur.execute("INSERT INTO user_accounts(username, userid, password, email) VALUES(%s, %s, %s, %s)"
                    ,(username, userid, hash_password, email))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.')
        return jsonify({'message': 'User registered successfully!'}), 201
@func_set_timeout(3)  # 设定函数超执行时间_
# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.json
        userid = userDetails['userid']
        password = userDetails['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_accounts WHERE userid = %s", [userid])
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['username'] = user['username']
            username = user['username']
            flash('You are now logged in!')
            return jsonify({'message': f'欢迎登录! {username}'})
        else:
            flash('Login Unsuccessful. Please check userid and password')
            return jsonify({'message': f'用户名或密码错误'})
        
@func_set_timeout(3)  # 设定函数超执行时间_
# 用户仪表板
def dashboard():
    if not session.get('loggedin'):
        return '请先登录'
    return 'Welcome ' + session.get('username')

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/send_new')
def send_new():
    return render_template('newsend.html')

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/send_test')
def send_test():
    return render_template('sendmsg.html')

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/h5_test')
def h5_test():
    return render_template('h5.html')

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/download/<filename>')
def download_file(filename):
    directory = "./downloads"  # 更改为你的文件存放目录
    return send_from_directory(directory, filename, as_attachment=True)

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/download-app')
def download_app():
    # 确保路径是正确的，并且 Flask 有足够的权限访问这个文件
    path_to_apk = "./downloads"
    filename = 'app-release.apk'
    return send_from_directory(path_to_apk, filename, as_attachment=True)

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/generate-qr')
def generate_qr():
    # 这里的 URL 替换成你的应用下载链接或任何你希望二维码指向的链接
    data = "https://www.212314.xyz/download/app-release.apk"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/')
def index():
    return render_template('show.html')

# 定义路由
@app.route('/sendmsg_task', methods=['GET', 'POST'])
def sendmsg_task():
    if request.method == 'POST':
        userDetails = request.json
        data = {}
        data['name'] = userDetails['name']
        data['time'] = userDetails['time']
        data['desc'] = userDetails['desc']
        data['stau'] = userDetails['stau']
        data['note'] = userDetails['note']
        wxopenid_list = []

        try:
            # 执行 SQL 查询
            cur = mysql.connection.cursor()
            cur.execute("SELECT wxopenid FROM test_wechat")
            
            # 获取查询结果
            results = cur.fetchall()
            print(results)
            # 将查询结果放入列表
            for row in results:
                print(row['wxopenid'])
                wxopenid_list.append(row['wxopenid'])

            # 关闭游标和数据库连接
            cur.close()
            access_token = get_access_token()
            print(access_token)
            print(wxopenid_list)
            send_message_task(access_token['access_token'],wxopenid_list,data)
            # 返回包含 wxopenid 的 JSON 响应
            return jsonify({"wxopenid": wxopenid_list})
        # finally:
        #     return jsonify({"error": "e"})
        except Exception as e:
            return jsonify({"error": str(e)})
        

# 定义路由
@app.route('/sendmsg_exam', methods=['GET', 'POST'])
def sendmsg_exam():
    if request.method == 'POST':
        userDetails = request.json
        data = {}
        data['name'] = userDetails['name']
        data['time'] = userDetails['time']
        data['posi'] = userDetails['posi']
        data['duri'] = userDetails['duri']
        data['note'] = userDetails['note']
        wxopenid_list = []

        try:
            # 执行 SQL 查询
            cur = mysql.connection.cursor()
            cur.execute("SELECT wxopenid FROM test_wechat")
            
            # 获取查询结果
            results = cur.fetchall()
            print(results)
            # 将查询结果放入列表
            for row in results:
                print(row['wxopenid'])
                wxopenid_list.append(row['wxopenid'])

            # 关闭游标和数据库连接
            cur.close()
            access_token = get_access_token()
            print(access_token)
            print(wxopenid_list)
            send_message_exam(access_token['access_token'],wxopenid_list,data)
            # 返回包含 wxopenid 的 JSON 响应d
            return jsonify({"wxopenid": wxopenid_list})
        # finally:
        #     return jsonify({"error": "e"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
        

# 定义路由
@app.route('/sendmsg_course', methods=['GET', 'POST'])
def sendmsg_course():
    if request.method == 'POST':
        userDetails = request.json
        data = {}
        data['name'] = userDetails['name']
        data['time'] = userDetails['time']
        data['posi'] = userDetails['posi']
        data['teac'] = userDetails['teac']
        data['note'] = userDetails['note']
        wxopenid_list = []

        try:
            # 执行 SQL 查询
            cur = mysql.connection.cursor()
            cur.execute("SELECT wxopenid FROM test_wechat")
            
            # 获取查询结果
            results = cur.fetchall()
            print(results)
            # 将查询结果放入列表
            for row in results:
                print(row['wxopenid'])
                wxopenid_list.append(row['wxopenid'])

            # 关闭游标和数据库连接
            cur.close()
            access_token = get_access_token()
            print(access_token)
            print(wxopenid_list)
            send_message_course(access_token['access_token'],wxopenid_list,data)
            # 返回包含 wxopenid 的 JSON 响应d
            return jsonify({"wxopenid": wxopenid_list})
        # finally:
        #     return jsonify({"error": "e"})
        except Exception as e:
            return jsonify({"error": str(e)})
        
@func_set_timeout(3)  # 设定函数超执行时间_
def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': 'wx4272c218ad712121',
        'secret': "4a35ef05c3ab78b03c38aa66971cd4be",
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result

@func_set_timeout(3)  # 设定函数超执行时间_
def send_message_task(access_token, openid_list,data):
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + access_token

    headers = {
        'Content-Type': 'application/json'
    }

    template_data = {
        "touser": "",
        "template_id": "e4E-yonmX6IxU1ppW6E0zsbg-9XaSGKv9hx0HiypYT8",
        "page": "index",
        "data": {
            "thing5": {
                "value": data['name']
            },
            "date4": {
                "value": data['time']
            },
            "thing9": {
                "value": data['desc']
            },
            "phrase24": {
                "value": data['stau']
            },
            "thing7": {
                "value": data['note']
            }
        }
    }

    for openid in openid_list:
        print(openid)
        template_data["touser"] = openid
        payload = json.dumps(template_data)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)


@func_set_timeout(3)  # 设定函数超执行时间_
def send_message_exam(access_token, openid_list,data):
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + access_token

    headers = {
        'Content-Type': 'application/json'
    }

    template_data = {
        "touser": "",
        "template_id": "fGc0xxY0vrW1sz1EnHjn1wrAgUEG4vneMnb0ZevTwaU",
        "page": "index",
        "data": {
            "thing2": {
                "value": data['name']
            },
            "date3": {
                "value": data['time']
            },
            "thing13": {
                "value": data['posi']
            },
            "thing18": {
                "value": data['duri']
            },
            "thing12": {
                "value": data['note']
            }
        }
    }

    for openid in openid_list:
        print(openid)
        template_data["touser"] = openid
        payload = json.dumps(template_data)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        
        
@func_set_timeout(3)  # 设定函数超执行时间_
def send_message_course(access_token, openid_list,data):
    url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=" + access_token

    headers = {
        'Content-Type': 'application/json'
    }

    template_data = {
        "touser": "",
        "template_id": "5CQypJimZbhGQhwDwGswK6uI3Jf8IxTU2y_SfakzNcM",
        "page": "index",
        "data": {
            "thing4": {
                "value": data['name']
            },
            "time1": {
                "value": data['time']
            },
            "thing2": {
                "value": data['posi']
            },
            "thing3": {
                "value": data['teac']
            },
            "thing5": {
                "value": data['note']
            }
        }
    }

    for openid in openid_list:
        print(openid)
        template_data["touser"] = openid
        payload = json.dumps(template_data)
        response = requests.post(url, headers=headers, data=payload)
        print(response.text)
        
@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/wxlogin', methods=['POST'])
def wxlogin():
    print(request)
    data = request.json
    print(data)
    wxcode = data['code']
    print(wxcode)
    result = get_openid(wxcode)
    print("result"+str(result))
    cur = mysql.connection.cursor()
    ret = cur.execute("SELECT * FROM test_wechat WHERE wxopenid = %s", [result['openid']])
    if ret ==0:
        cur.execute("INSERT INTO test_wechat (wxopenid) VALUES (%s)", (result['openid'],))
        mysql.connection.commit()
    cur.close()
    # data = json.loads(result)
    if('openid' in result):
        return jsonify({'openid': result['openid']}), 201
    else:
        return jsonify({'errmsg': result['errmsg']}), 201

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/bindwxlogin', methods=['POST'])
def bindwxlogin():
    print(request)
    data = request.json
    print(data)
    wxcode = data['code']
    userid = data['userid']
    password = data['password'].encode('utf-8')
    print(wxcode+userid+str(password))
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM user_accounts WHERE userid = %s", [userid])
    user = cur.fetchone()
    print("userid"+str(user['userid']))
    cur.close()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 400
    if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
        
        reopenid = get_openid(wxcode)
        print("openid"+str(reopenid))
        
        # data = json.loads(result)
        if('openid' in reopenid):
            cur = mysql.connection.cursor()
            wxresult = cur.execute("SELECT * FROM user_wechat WHERE userid = %s", [user['userid']])
            print(wxresult)
            cur.close()
            if wxresult >0:
                cur.close()
                return jsonify({'msg':"已经绑定了"}), 500
            try:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO user_wechat (userid, wxopenid) VALUES (%s, %s)", (user['userid'], reopenid['openid']))
                mysql.connection.commit()
                cur.close()
                return jsonify({'openid': reopenid['openid'],'msg':"绑定成功"}), 201
            except Exception as e:
                print(str(e))
                return jsonify({'msg':"绑定失败",'error': str(e)}), 500
        else:
            return jsonify({'msg':"绑定失败",'errmsg': reopenid['errmsg']}), 500

@func_set_timeout(3)  # 设定函数超执行时间_
@app.route('/wxgetbind', methods=['POST'])
def wxgetbind():
    print(request)
    data = request.json
    print(data)
    wxcode = data['code']
    print(wxcode)
    result = get_openid(wxcode)
    print("result"+str(result))
    # data = json.loads(result)
    if('openid' in result):
        cur = mysql.connection.cursor()
        wxresult = cur.execute("SELECT * FROM user_wechat WHERE wxopenid = %s", [result['openid']])
        print(wxresult)
        if wxresult >0:
            wxuser = cur.fetchone()
            print(wxuser)
            tmpresult = cur.execute("SELECT * FROM user_accounts WHERE userid = %s", [wxuser['userid']])
            user = cur.fetchone()
            print(user)
            cur.close()
            return jsonify({'userid':wxuser['userid'],'username':user['username'],'email':user['email']}), 201
        else:
            return jsonify({'msg':"null"})
    #     return jsonify({'openid': result['openid']}), 201
    # else:
    #     return jsonify({'errmsg': result['errmsg']}), 201
    
@func_set_timeout(3)  # 设定函数超执行时间_
def get_openid(js_code):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': 'wx4272c218ad712121',
        'secret': '4a35ef05c3ab78b03c38aa66971cd4be',
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)
