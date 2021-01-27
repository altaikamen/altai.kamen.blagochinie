from flask import Flask, render_template
from app import random_quote as rq
from app import article as a
from icecream import ic

app = Flask(__name__)

all_articles = a.get_article()
last_article_id = all_articles[-1][0]

first_articles = {'first_id': 0, 'last_id': 10, 'last_index': last_article_id, 'min': True, 'max': False}
now_articles = {}


@app.route('/')
@app.route('/main_page/')
def index():
    first_id = first_articles['first_id']
    last_id = first_articles['last_id']

    return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[first_id:last_id],
                           now_articles=first_articles)


@app.route('/contact/')
def contact():
    return render_template('sections\\contact.html', quote=rq.get_random_quote())


@app.route('/archbishop/')
def archbishop():
    return render_template('sections\\archbishop.html', quote=rq.get_random_quote())


@app.route('/clergy/')
def clergy():
    return render_template('clergy\\clerics_menu.html', quote=rq.get_random_quote())


@app.route('/churches/')
def churches():
    return render_template('churches\\churches_menu.html', quote=rq.get_random_quote())


@app.route('/about/')
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


@app.route('/<string:post>/')
def watch_post(post):
    post = {'title': 'КакойНибудьЗаголовок', 'article': 'КакБыПримерСтатьи'}
    return render_template('post.html', quote=rq.get_random_quote(), post=post)


@app.route('/page<int:id>/')
def next_page(id):
    global now_articles

    # для самой первой страницы
    if id == 1:
        first_id = 10
        last_id = 20

        id += 1

        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'next_id': id,
                        'min': False, 'max': False}

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)

    # для последующих страниц
    first_id = now_articles['first_id'] + 10
    last_id = first_id + 10

    id += 1

    # для самой последней страницы
    if last_id >= last_article_id:
        first_id = last_article_id - 10

        id = str(last_article_id)[0]
        id = int(id)

        now_articles = {'first_id': first_id, 'last_id': last_article_id, 'last_index': last_article_id, 'next_id': id,
                        'min': False, 'max': True}

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)
    else:
        # для последующих страниц
        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'next_id': id,
                        'min': False, 'max': False}

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)


@app.route('/page<int:id>/')
def last_page(id):
    global now_articles

    first_id = now_articles['first_id'] - 10
    last_id = now_articles['last_id'] - 10

    if first_id <= 0:
        # для самой первой страницы
        first_id = 1
        last_id = 11
        id = 1

        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'id': id,
                        'min': False, 'max': False}
        ic(now_articles)

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)
    else:
        # для последующих страниц
        id -= 1

        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'id': id,
                        'min': False, 'max': False}

        ic(now_articles)

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)
