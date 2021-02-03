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


def get_databases():
    # TODO: обработать БД и сортировать по дате
    def get_posts(path, query):
        tuple_posts = db.pull_data(path, query)

        dict_posts = []

        for post in tuple_posts:
            if post[7]:
                images = post[7].split(', ')
            else:
                images = None

            # деление post по '\n' для того, что бы текст был абзацами, а не строкой
            dict_posts.append({'id': post[0], 'data': post[1], 'link': post[2], 'title': post[3], 'preview_image': post[4],
                               'preview': post[5], 'post': post[6].split('\n'), 'images': images})

        # сортировка по дате
        # DateList.sort(key=lambda date: datetime.strptime(date, '%d.%m.%Y'))

        return dict_posts

    articles_database = get_posts('app\\static\\databases\\articles.sqlite', 'SELECT * from articles')
    saints_databases = get_posts('app\\static\\databases\\saints.sqlite', 'SELECT * from saints')
    our_events_databases = get_posts('app\\static\\databases\\our_events.sqlite', 'SELECT * from our_events')
    all_church_events_databases = get_posts('app\\static\\databases\\all_church_events.sqlite', 'SELECT * from all_church_events')

    return all_church_events_databases, our_events_databases, articles_database, saints_databases


def get_all_posts():
    # TODO: обработать все БД и сортировать по дате
    all_church_events_databases, our_events_databases, articles_database, saints_databases = get_databases()
    all_posts = articles_database + saints_databases + our_events_databases + all_church_events_databases

    return all_posts


db = DataBase()
