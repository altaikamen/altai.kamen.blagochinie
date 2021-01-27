import sqlite3


class DataBase:
    def create_connection(self, path):
        return sqlite3.connect(path)

    def update_data(self, path, query):
        connection = self.create_connection(path)

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def pull_data(self, path):
        query = 'SELECT * from articles'
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


def get_article():
    db = DataBase()
    data = db.pull_data('app\\static\\databases\\articles.sqlite')

    return data
