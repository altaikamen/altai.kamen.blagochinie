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


def get_databases():
    def get_posts(path, query):
        tuple_posts = db.pull_data(path, query)

        posts = []
        for post in tuple_posts:
            if post[7]:
                images = post[7].split(', ')
            else:
                images = None

            # деление post по '\n' для того, чтобы текст был абзацами, а не строкой
            posts.append({'id': post[0], 'date': post[1], 'link': post[2], 'title': post[3], 'preview_image': post[4],
                               'preview': post[5], 'post': post[6].split('\n'), 'images': images})

        sorted_posts = sort_posts(posts)

        return sorted_posts

    articles_database = get_posts('app\\static\\databases\\articles.sqlite', 'SELECT * from articles')
    saints_databases = get_posts('app\\static\\databases\\saints.sqlite', 'SELECT * from saints')
    our_events_databases = get_posts('app\\static\\databases\\our_events.sqlite', 'SELECT * from our_events')
    all_church_events_databases = get_posts('app\\static\\databases\\all_church_events.sqlite', 'SELECT * from all_church_events')

    return all_church_events_databases, our_events_databases, articles_database, saints_databases


def get_all_posts():
    all_church_events_databases, our_events_databases, articles_database, saints_databases = get_databases()
    all_posts = articles_database + saints_databases + our_events_databases + all_church_events_databases

    sorted_all_posts = sort_posts(all_posts)

    return sorted_all_posts


db = DataBase()
