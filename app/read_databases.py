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

    def create_database(self):
        # создание таблиц
        table = """
                    CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        link TEXT,
                        preview TEXT,
                        article TEXT
                    );
                """

        self.update_data('articles.sqlite', table)

        for i in [str('статья ' + str(elem)) for elem in range(1, 50)]:
            article = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Nisl tincidunt eget nullam non. Quis hendrerit dolor magna eget est lorem ipsum dolor sit. Volutpat odio facilisis mauris sit amet massa. Commodo odio aenean sed adipiscing diam donec adipiscing tristique. Mi eget mauris pharetra et. Non tellus orci ac auctor augue. Elit at imperdiet dui accumsan sit. Ornare arcu dui vivamus arcu felis. Egestas integer eget aliquet nibh praesent. In hac habitasse platea dictumst quisque sagittis purus. Pulvinar elementum integer enim neque volutpat ac."
            query = f"""
                        INSERT INTO
                            articles (title, link, preview, article)
                        VALUES
                            ('{i}', '{i}', '{article}', '{article}');
                    """

            self.update_data('articles.sqlite', query)


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
