from flask import Flask, render_template
from app import random_quote as rq
from app import article as all_articles
from icecream import ic

app = Flask(__name__)

articles = all_articles.get_articles()
last_articles_index = articles[-1][0]

first_page = {'first_id': 0, 'last_id': 10, 'last_index': last_articles_index, 'min': True, 'max': False}
page_data = {}


@app.route('/')
@app.route('/main_page/')
def index():
    first_id = first_page['first_id']
    last_id = first_page['last_id']
    posts = articles[first_id:last_id]

    return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=first_page)


@app.route('/contact/')
def contact():
    return render_template('sections/contact.html', quote=rq.get_random_quote())


@app.route('/archbishop/')
def archbishop():
    return render_template('sections/archbishop.html', quote=rq.get_random_quote())


@app.route('/clergy/')
def clergy():
    return render_template('clergy/clerics_menu.html', quote=rq.get_random_quote())


@app.route('/churches/')
def churches():
    return render_template('churches/churches_menu.html', quote=rq.get_random_quote())


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
    global page_data

    first_id = id * 10
    last_id = first_id + 10

    id += 1

    if last_id >= last_articles_index:  # для самой последней страницы
        first_id = last_articles_index - 10

        id = str(last_articles_index)[0]
        id = int(id)

        posts = articles[first_id:last_id]
        page_data = {'first_id': first_id, 'last_id': last_articles_index, 'last_index': last_articles_index, 'id': id,
                        'min': False, 'max': True}

        return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)

    else:  # для последующих страниц
        posts = articles[first_id:last_id]
        page_data = {'first_id': first_id, 'last_id': last_id, 'last_index': last_articles_index, 'id': id,
                        'min': False, 'max': False}

        return render_template('index.html', quote=rq.get_random_quote(), posts=posts, page=page_data)


@app.route('/page<int:id>/')
def last_page(id):
    global page_data

    first_id = page_data['first_id'] - 10
    last_id = page_data['last_id'] - 10

    if first_id <= 0:
        # для самой первой страницы
        first_id = 1
        last_id = 11
        id = 1

        page_data = {'first_id': first_id, 'last_id': last_id, 'last_index': last_articles_index, 'id': id,
                        'min': False, 'max': False}
        ic(page_data)

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=articles[first_id:last_id],
                               now_articles=page_data)
    else:
        # для последующих страниц
        id -= 1

        page_data = {'first_id': first_id, 'last_id': last_id, 'last_index': last_articles_index, 'id': id,
                        'min': False, 'max': False}

        ic(page_data)

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=articles[first_id:last_id],
                               now_articles=page_data)
