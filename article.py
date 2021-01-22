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
                        article TEXT
                    );
                """

        self.update_data('articles.sqlite', table)

        for article in [str('статья ' + str(elem)) for elem in range(1, 50)]:
            query = f"""
                        INSERT INTO
                            articles (article)
                        VALUES
                            ('{article}');
                    """

            self.update_data('articles.sqlite', query)


def get_article():
    db = DataBase()
    data = db.pull_data('app\\static\\databases\\articles.sqlite')

    return data
