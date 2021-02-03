from flask import Flask, render_template, url_for, redirect, request
import re
from app import random_quote as rq
from app import read_databases
from icecream import ic

app = Flask(__name__)

all_church_events_databases, our_events_databases, articles_database, saints_databases = read_databases.get_databases()
all_posts = read_databases.get_all_posts()

active_databases = all_posts  # нужна для того, что бы не передавать много аргументов
active_sub_title = ''


# используется для первой страницы в рубриках
# нужно для тех случаев, когда постов меньше 10 в рубрики и создавать кнопки не надо
def get_page_data():
    tuple_posts = active_databases[0:11]

    if len(tuple_posts) <= 10:
        page_data = {'past_id': None, 'id': 0, 'next_id': 1, 'min': True, 'max': False, 'over_ten': False}
    else:
        page_data = {'past_id': None, 'id': 0, 'next_id': 1, 'min': True, 'max': False, 'over_ten': True}

    return page_data


@app.route('/')
@app.route('/main_page')
def main_page():
    global active_databases, active_sub_title

    active_databases = all_posts
    active_sub_title = 'Все события'

    posts = active_databases[0:10]
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title='Официальный Сайт Каменского Благочиния Славгородской Епархии')


@app.route('/all_church_events')
def all_church_events():
    global active_databases, active_sub_title

    active_databases = all_church_events_databases
    active_sub_title = 'Общецерковные события'

    posts = active_databases[0:10]
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title='Общецерковные События | Каменское Благочиние Славгородской Епархии')


@app.route('/our_events')
def our_events():
    global active_databases, active_sub_title

    active_databases = our_events_databases
    active_sub_title = 'События благочиния'

    posts = active_databases[0:10]
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title='События Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/articles')
def articles():
    global active_databases, active_sub_title

    active_databases = articles_database
    active_sub_title = 'Статьи'

    posts = active_databases[0:10]
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title='Статьи | Каменское Благочиние Славгородской Епархии')


@app.route('/saints')
def saints():
    global active_databases, active_sub_title

    active_databases = saints_databases
    active_sub_title = 'Святые о...'

    posts = active_databases[0:10]
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title='Святые о... | Каменское Благочиние Славгородской Епархии')


@app.route('/post/<post_link>')
def post(post_link):
    post = {}

    for dict_post in all_posts:
        if dict_post['link'] == post_link:
            post = dict_post

    return render_template('post.html', quote=rq.get_random_quote(), post=post, title=post['title'])


@app.route('/page<int:id>/')
def next_page(id):
    past_id = id - 1
    next_id = id + 1

    latest_index = active_databases.index(active_databases[-1]) + 1  # потому что в списке индексы с нуля, а в срезе с 1
    latest_id = int(str(latest_index)[0])

    # для последней страницы
    if id >= latest_id:
        last_index = latest_index

        if last_index <= 10:  # если последняя страница - единственная в рубрике
            page_data = {'past_id': None, 'id': latest_id, 'next_id': None, 'min': True, 'max': False, 'over_ten': False}
            posts = active_databases[0:latest_index]
        else:
            start_index = latest_id * 10
            posts = active_databases[start_index:latest_index]

            past_id = latest_id - 1
            page_data = {'past_id': past_id, 'id': latest_id, 'next_id': None, 'min': False, 'max': True, 'over_ten': True}

        return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                               sub_title=active_sub_title,
                               title=f'Страница {latest_id} | Каменское Благочиние Славгородской Епархии')

    # для не крайних страниц
    start_index = id * 10
    last_index = start_index + 10
    posts = active_databases[start_index:last_index]

    # для того что бы не было отрицательных значений у post_id
    if past_id < 0:
        page_data = {'past_id': None, 'id': id, 'next_id': next_id, 'min': True, 'max': False, 'over_ten': True}
    else:
        page_data = {'past_id': past_id, 'id': id, 'next_id': next_id, 'min': False, 'max': False, 'over_ten': True}

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title=active_sub_title,
                           title=f'Страница {id} | Каменское Благочиние Славгородской Епархии')


@app.route('/page<int:id>/')
def past_page(id):
    past_id = id - 1
    next_id = id + 1

    # для первой страницы
    if id <= 0:
        return redirect(url_for('main_page'))

    # для не крайних страниц
    start_index = past_id * 10
    last_index = start_index + 10
    posts = active_databases[start_index:last_index]

    page_data = {'past_id': past_id, 'id': id, 'next_id': next_id, 'min': False, 'max': False, 'over_ten': True}

    render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                    sub_title=active_sub_title,
                    title=f'Страница {id} | Каменское Благочиние Славгородской Епархии')


@app.route('/search', methods=['POST', 'GET'])
def search():
    global active_databases

    search_box = ''
    posts = []

    if request.method == 'POST':
        search_box = request.form.get('search_box')  # запрос к данным формы

    for post in all_posts:
        for text in post.values():
            match = re.search(search_box.lower(), str(text).lower())
            if match:
                posts.append(post)
                continue

    active_databases = posts
    page_data = get_page_data()

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data,
                           sub_title='Результаты поиска по архиву',
                           title='Поиск По Архиву | Каменское Благочиние Славгородской Епархии')


@app.route('/contact')
def contact():
    return render_template('sections/contact.html', quote=rq.get_random_quote(),
                           title='Контактная Информация | Каменское Благочиние Славгородской Епархии')


@app.route('/archbishop')
def archbishop():
    return render_template('sections/archbishop.html', quote=rq.get_random_quote(),
                           title='Правящий Архиерей | Каменское Благочиние Славгородской Епархии')


@app.route('/clergy/')
def clergy():
    return render_template('clergy/clerics_menu.html', quote=rq.get_random_quote(),
                           title='Духовенство Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/churches/')
def churches():
    return render_template('churches/churches_menu.html', quote=rq.get_random_quote(),
                           title='Храмы Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/about')
def about():
    return render_template('dev_page.html', quote=rq.get_random_quote(),
                           title='О Благочинии | Каменское Благочиние Славгородской Епархии')
