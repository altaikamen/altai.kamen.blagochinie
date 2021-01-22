from flask import Flask, render_template, url_for
from app import random_quote as rq
from app import article as a

app = Flask(__name__)

all_articles = a.get_article()
last_elem_index = all_articles[-1][0]

first_index = 0
last_index = 10

id = str(first_index)[-1]


@app.route('/')
@app.route('/page')
def index():
    return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[0:10])


@app.route('/contact')
def contact():
    return render_template('sections\\contact.html', quote=rq.get_random_quote())


@app.route('/archbishop')
def archbishop():
    return render_template('sections\\archbishop.html', quote=rq.get_random_quote())


@app.route('/clergy')
def clergy():
    return render_template('clergy\\clerics_menu.html', quote=rq.get_random_quote())


@app.route('/churches')
def churches():
    return render_template('churches\\churches_menu.html', quote=rq.get_random_quote())


@app.route('/about')
def about():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/all_church_events')
def all_church_events():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/our_events')
def our_events():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/articles')
def articles():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/saints')
def saints():
    return render_template('dev_page.html', quote=rq.get_random_quote())


@app.route('/addiction')
@app.route('/page_<int:id>')
def addiction(id):
    global first_index, last_index

    first_index += 10
    last_index += 10

    if last_index >= last_elem_index:
        if first_index < last_elem_index:
            return render_template('last_more.html', quote=rq.get_random_quote(), posts=all_articles[first_index:last_elem_index])
    else:
        return render_template('central_more.html', quote=rq.get_random_quote(), posts=all_articles[first_index:last_index])


@app.route('/delete')
def delete():
    global first_index, last_index

    first_index -= 10
    last_index -= 10

    if first_index <= 0:
        return render_template('index.html', quote=rq.get_random_quote(), posts=all_articles[0:10])
    else:
        return render_template('central_more.html', quote=rq.get_random_quote(), posts=all_articles[first_index:last_index])
