import re
from flask import Flask, render_template, url_for, redirect, request, abort
from icecream import ic
from app import random_quote as rq
from app import databases

app = Flask(__name__)

active_page_title = ''


# нужно для тех случаев, когда постов меньше 10 в рубрики и создавать кнопки может быть не надо
def get_page_data(section):
    if section == 'all_posts':
        database = databases.get_all_posts()
    else:
        database = databases.get_section(section)

    posts = database[0:11]

    if len(posts) <= 10:
        page_data = {'past_id': None, 'id': 0, 'next_id': 1, 'min': True, 'max': False, 'over_ten': False}
    else:
        page_data = {'past_id': None, 'id': 0, 'next_id': 1, 'min': True, 'max': False, 'over_ten': True}

    return page_data


@app.route('/')
@app.route('/main_page')
def main_page():
    global active_page_title

    active_page_title = 'Все события'
    section = 'all_posts'

    all_posts = databases.get_all_posts()
    posts = all_posts[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title='Официальный Сайт Каменского Благочиния Славгородской Епархии')


@app.route('/all_church_events/')
def all_church_events():
    global active_page_title

    active_page_title = 'Общецерковные события'
    section = 'all_church_events'

    all_church_events_database = databases.get_section('all_church_events')
    posts = all_church_events_database[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title='Общецерковные События | Каменское Благочиние Славгородской Епархии')


@app.route('/our_events/')
def our_events():
    global active_page_title

    active_page_title = 'События благочиния'
    section = 'our_events'

    our_events_database = databases.get_section('our_events')
    posts = our_events_database[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title='События Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/articles/')
def articles():
    global active_page_title

    active_page_title = 'Статьи'
    section = 'articles'

    articles_database = databases.get_section('articles')
    posts = articles_database[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title='Статьи | Каменское Благочиние Славгородской Епархии')


@app.route('/saints/')
def saints():
    global active_page_title

    active_page_title = 'Святые о...'
    section = 'saints'

    saints_database = databases.get_section('saints')
    posts = saints_database[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title='Святые о... | Каменское Благочиние Славгородской Епархии')


@app.route('/churches/')
def churches():
    global active_page_title

    churches_database = databases.get_parish('churches')

    return render_template('parish.html', random_quote=rq.get_random_quote(), parishes=churches_database,
                           section='churches',
                           page_title='Храмы благочиния',
                           tab_title='Храмы Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/clergy/')
def clergy():
    global active_page_title

    clergy_database = databases.get_parish('clergy')

    return render_template('parish.html', random_quote=rq.get_random_quote(), parishes=clergy_database,
                           section='clergy',
                           page_title='Духовенство',
                           tab_title='Духовенство Благочиния | Каменское Благочиние Славгородской Епархии')


@app.route('/archbishop')
def archbishop():
    return render_template('archbishop.html', random_quote=rq.get_random_quote(),
                           tab_title='Правящий Архиерей | Каменское Благочиние Славгородской Епархии')


@app.route('/about')
def about():
    return render_template('about.html', random_quote=rq.get_random_quote(),
                           tab_title='О Благочинии | Каменское Благочиние Славгородской Епархии')


@app.route('/contact')
def contact():
    return render_template('contact.html', random_quote=rq.get_random_quote(),
                           tab_title='Контактная Информация | Каменское Благочиние Славгородской Епархии')


@app.route('/<section>/<link>')
def post(section, link):
    post = {}

    if section == 'clergy' or section == 'churches':
        database = databases.get_parish(section)
    else:
        database = databases.get_all_posts()

    for posts in database:
        if posts['link'] == link:
            post = posts

    tag_text = ''
    for string in post['post']:
        tag_text += f'<p>{string}</p>\n'

    if post['date']:
        date = post['date']
    else:  # для /clergy и /churches
        date = ''

    # просто разные стили постов
    tag_images = ''
    if post['images']:
        for image in post['images']:
            tag_images += f'<img class="post-image" src="../static/images/post_images/{image}">'

        html = f"""
                    <div class="date"><i>{date}</i></div>
                    <h2 class="title">{post['title']}</h2>
                    <hr width="80%" color="#c09669">

                    <article>
                      {tag_text}
                      {tag_images}
                    </article>
                """
    else:
        if post['preview_image']:
            preview_image = post['preview_image']
            tag_preview_image = ''
            if section == 'clergy' or section == 'churches':
                tag_preview_image += f'<img class="cleric-image" src="../static/images/post_images/{preview_image}">'
            else:
                tag_preview_image += f'<img class="post-image" src="../static/images/post_images/{preview_image}">'
            html = f"""
                        <div class="date"><i>{date}</i></div>
                        <h2 class="title">{post['title']}</h2>
                        <hr width="80%" color="#c09669">

                        <article>
                          {tag_preview_image}
                          {tag_text}
                        </article>
                    """
        else:
            html = f"""
                        <div class="date"><i>{date}</i></div>
                        <h2 class="title">{post['title']}</h2>
                        <hr width="80%" color="#c09669">
                        <article>
                          {tag_text}
                        </article>
                    """

    with open('app/templates/post_text.html', 'w', encoding='utf-8') as file:
        file.write(html)

    return render_template('post.html', random_quote=rq.get_random_quote(), tab_title=post['title'])


@app.route('/<section>/page<int:id>')
def page(section, id):
    # для первых страниц
    if id <= 0:
        if section == 'all_posts':
            return redirect(url_for('main_page'))
        elif section == 'all_church_events':
            return redirect(url_for('all_church_events'))
        elif section == 'our_events':
            return redirect(url_for('our_events'))
        elif section == 'articles':
            return redirect(url_for('articles'))
        elif section == 'saints':
            return redirect(url_for('saints'))
        elif section == 'search':
            return redirect(url_for('search'))

    if section == 'all_posts':
        database = databases.get_all_posts()
    else:
        database = databases.get_section(section)

    latest_index = database.index(database[-1]) + 1  # потому что в списке индексы с нуля, а в срезе с 1
    latest_id = int(str(latest_index)[0])

    # для последних страниц
    if id >= latest_id:
        last_index = latest_index

        if last_index <= 10:  # если последняя страница - единственная в рубрике
            page_data = {'id': latest_id, 'min': True, 'max': False, 'over_ten': False}
            posts = database[0:latest_index]
        else:
            start_index = latest_id * 10
            posts = database[start_index:latest_index]

            page_data = {'id': latest_id, 'min': False, 'max': True, 'over_ten': True}

        return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                               section=section,
                               page_title=active_page_title,
                               tab_title=f'Страница {latest_id} | Каменское Благочиние Славгородской Епархии')

    # для не крайних страниц
    start_index = id * 10
    last_index = start_index + 10
    posts = database[start_index:last_index]

    # для того что бы не было отрицательных значений у id
    if id - 1 < 0:
        page_data = {'id': id, 'min': True, 'max': False, 'over_ten': True}
    else:
        page_data = {'id': id, 'min': False, 'max': False, 'over_ten': True}

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section=section,
                           page_title=active_page_title,
                           tab_title=f'Страница {id} | Каменское Благочиние Славгородской Епархии')


@app.route('/start_search', methods=['POST'])
def start_search():
    search_box = ''
    match_list = []

    if request.method == 'POST':
        search_box = request.form.get('search_box')  # запрос к данным формы

    pattern_list = search_box.split()

    all_posts = databases.get_all_posts()
    for post in all_posts:
        for text in post.values():
            for pattern in pattern_list:
                match = re.search(pattern.lower(), str(text).lower())
                if match:
                    if post not in match_list:  # чтобы не добавлялось одно и тоже
                        match_list.append(post)
                    break

    databases.update_search(match_list)

    return redirect(url_for('search'))


@app.route('/search')
def search():
    global active_page_title

    search_database = databases.get_section('search')
    active_page_title = 'Результаты поиска по архиву'
    section = 'search'

    posts = search_database[0:10]
    page_data = get_page_data(section)

    return render_template('index.html', random_quote=rq.get_random_quote(), posts=posts, page=page_data,
                           section='search',
                           page_title=active_page_title,
                           tab_title='Поиск По Архиву | Каменское Благочиние Славгородской Епархии')
