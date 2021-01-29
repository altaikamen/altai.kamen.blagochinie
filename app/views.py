from flask import Flask, render_template, redirect, url_for
from app import random_quote as rq
from app import read_databases
from icecream import ic

app = Flask(__name__)

articles_database = read_databases.get_articles('app\\static\\databases\\articles.sqlite')
active_databases = articles_database

latest_index = active_databases[-1][0]
latest_id = int(str(latest_index)[0])


@app.route('/')
@app.route('/main_page')
def main_page():
    global active_databases
    active_databases = articles_database
    page_data = {'id': 0, 'next_id': 1, 'min': True, 'max': False}
    posts = active_databases[0:10]

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)


@app.route('/contact')
def contact():
    return render_template('sections/contact.html', quote=rq.get_random_quote())


@app.route('/archbishop')
def archbishop():
    return render_template('sections/archbishop.html', quote=rq.get_random_quote())


@app.route('/clergy/')
def clergy():
    return render_template('clergy/clerics_menu.html', quote=rq.get_random_quote())


@app.route('/churches/')
def churches():
    return render_template('churches/churches_menu.html', quote=rq.get_random_quote())


@app.route('/about')
def about():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/all_church_events/')
def all_church_events():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/our_events/')
def our_events():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/articles/')
def articles():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/saints/')
def saints():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/<post>')
def post(post):
    post = {'title': 'КакойНибудьЗаголовок', 'article': 'КакБыПримерСтатьи'}
    return render_template('post.html', quote=rq.get_random_quote(), post=post)


@app.route('/page<int:id>/')
def next_page(id):
    past_id = id - 1
    next_id = id + 1

    # для последней страницы
    if id >= latest_id:
        past_id = latest_id - 1
        page_data = {'past_id': past_id, 'id': latest_id, 'min': False, 'max': True}

        start_index = latest_id * 10
        last_index = latest_index
        posts = active_databases[start_index:last_index]

        return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)

    # для не крайних страниц
    start_index = id * 10
    last_index = start_index + 10
    posts = active_databases[start_index:last_index]

    # для
    if past_id < 0:
        page_data = {'id': id, 'next_id': next_id, 'min': True, 'max': False}
    else:
        page_data = {'past_id': past_id, 'id': id, 'next_id': next_id, 'min': False, 'max': False}

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)


@app.route('/page<int:id>/')
def past_page(id):
    past_id = id - 1
    next_id = id + 1

    # для первой страницы
    if id <= 0:
        main_page()

    # для не крайних страниц
    start_index = past_id * 10
    last_index = start_index + 10
    posts = active_databases[start_index:last_index]

    page_data = {'past_id': past_id, 'id': id, 'next_id': next_id, 'min': False, 'max': False}

    render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)
