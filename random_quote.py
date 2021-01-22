import sqlite3
import random


class DataBase:
    def create_connection(self, path):
        return sqlite3.connect(path)

    def update_data(self, path, query):
        connection = self.create_connection(path)

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def pull_data(self, path):
        query = 'SELECT * from quotes'
        connection = self.create_connection(path)

        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def create_database(self):

        # создание таблиц
        table = """
                    CREATE TABLE IF NOT EXISTS quotes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quote TEXT
                    );
                """

        self.update_data('app\\static\\databases\\quotes.sqlite', table)

        for quote in [str('фраза '+str(elem)) for elem in range(1, 100)]:
            query = f"""
                        INSERT INTO
                            quotes (quote)
                        VALUES
                            ('{quote}');
                    """

            self.update_data('app\\static\\databases\\quotes.sqlite', query)


def get_random_quote():
    db = DataBase()
    data = db.pull_data('app\\static\\databases\\quotes.sqlite')

    random_quote = random.choice(data)
    return random_quote[1]
