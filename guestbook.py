# coding : UTF-8
import shelve
from datetime import datetime
from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'

def save_data(name, comment, create_at):
    #shelveモジュールでデータベースファイルを開きます
    database = shelve.open(DATA_FILE)
    #データベースにgreeting_listが無ければ新規作成
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        #データベースからデータを取得
        greeting_list = database['greeting_list']
    #リストの先頭に投稿データを追加する
    greeting_list.insert(0, {'name':name, 'comment':comment, 'create_at':create_at})

    #データベースを更新
    database['greeting_list'] = greeting_list

    database.close()

def load_data():
    database = shelve.open(DATA_FILE)
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

@application.route('/')
def index():
    #トップページ
    greeting_list = load_data()
    return render_template('index.html', greeting_list=greeting_list)

@application.route('/post', methods=['POST'])
def post():
    # Get data
    name = request.form.get('name')
    comment = request.form.get('comment')
    create_at = datetime.now()
    #Save data
    save_data(name, comment, create_at)

    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
    return escape(s).replace('\n', Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')

if __name__ == '__main__':
    #IP is 127.0.0.1:8000
    application.run('127.0.0.1', 8000, debug=True)