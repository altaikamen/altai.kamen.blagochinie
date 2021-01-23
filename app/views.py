from flask import Flask, render_template
from app import random_quote as rq
from app import article as a

app = Flask(__name__)

all_articles = a.get_article()
last_article_id = all_articles[-1][0]

first_elem_index = 0
last_elem_index = 10

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


@app.route('/page<int:id>/')
def next_page(id):
    global now_articles

    print(id)

    """if id == 0:
        now_articles = {'first_id': 0, 'last_id': 10, 'last_index': last_article_id, 'id': 1, 'min': True, 'max': False}
        first_id = 0
        last_id = 10

        return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[first_id:last_id],
                               now_articles=now_articles)"""
    if id == 1:
        first_id = 11
        last_id = 20

        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'id': 2, 'min': False, 'max': False}
        print(now_articles)

        return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[first_id:last_id],
                               now_articles=now_articles)

    first_id = now_articles['first_id'] + 10
    last_id = first_id + 10

    id = str(first_id)[0]

    if last_id >= last_article_id:
        if first_id < last_article_id:
            first_id = last_article_id - 10

            now_articles = {'first_id': first_id, 'last_id': last_article_id, 'last_index': last_article_id,
                            'min': False, 'max': True}

            return render_template('index.html', quote=rq.get_random_quote(),
                                   posts=all_articles[first_id:last_article_id],
                                   now_articles=now_articles)
    else:
        now_articles = {'first_id': first_id, 'last_id': last_id, 'last_index': last_article_id, 'id': int(id),
                        'min': False, 'max': False}

        print(now_articles)

        return render_template('index.html', quote=rq.get_random_quote(),
                               posts=all_articles[first_id:last_id],
                               now_articles=now_articles)


@app.route('/last_page/')
def last_page():
    global first_elem_index, last_elem_index

    first_elem_index -= 10
    last_elem_index -= 10

    if first_elem_index <= 0:
        return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[0:10])
    else:
        return render_template('central_more.html', quote=rq.get_random_quote(), posts=all_articles[first_elem_index:last_elem_index])
