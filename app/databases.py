from datetime import datetime
import sqlite3


class DataBase:
    def create_connection(self, path):
        return sqlite3.connect(path)

    def update_data(self, path, query):
        connection = self.create_connection(path)

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def pull_data(self, path, query):
        connection = self.create_connection(path)

        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def delete_and_create_search(self, match_list):
        pass


db = DataBase()


def get_section(section):
    path = f'app\\static\\databases\\{section}.sqlite'
    query = f'SELECT * from {section}'
    tuple_posts = db.pull_data(path, query)

    posts = []
    for post in tuple_posts:
        if post[7]:
            images = post[7].split(', ')
        else:
            images = None

        # деление post по '\n' для того, чтобы текст был абзацами, а не строкой
        posts.append({'id': post[0], 'section': section, 'date': post[1], 'link': post[2], 'title': post[3],
                      'preview_image': post[4], 'preview_post': post[5], 'post': post[6].split('\n'), 'images': images})

    sorted_posts = sort_posts(posts)

    return sorted_posts


def get_parish(database):
    path = f'app\\static\\databases\\{database}.sqlite'
    query = f'SELECT * from {database}'
    tuple_parish = db.pull_data(path, query)

    parishes = []
    for parish in tuple_parish:
        parishes.append({'id': parish[0], 'link': parish[1], 'title': parish[2], 'image': parish[3]})

    return parishes


def sort_posts(posts):
    sorted_posts = []

    date_list = []
    for post in posts:
        date_list.append(post['date'])

    set_date_list = list(set(date_list))  # для того, чтобы не было одинаковых дат и посты не повторялись
    set_date_list.sort(key=lambda date: datetime.strptime(date, '%d.%m.%Y'))

    # добавление статей по порядку
    for date in set_date_list:
        for post in posts:
            if date == post['date']:
                sorted_posts.append(post)

    sorted_posts.reverse()  # чтобы сначала были новые посты, а потом старые

    return sorted_posts


def get_all_posts():
    all_church_events_databases = get_section('all_church_events')
    our_events_databases = get_section('our_events')
    articles_database = get_section('articles')
    saints_databases = get_section('saints')

    all_posts = articles_database + saints_databases + our_events_databases + all_church_events_databases
    sorted_all_posts = sort_posts(all_posts)

    return sorted_all_posts
