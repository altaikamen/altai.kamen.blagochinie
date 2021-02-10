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


db = DataBase()


def get_random_quote():
    data = db.pull_data('app\\static\\databases\\quotes.sqlite')

    random_quote = random.choice(data)
    return random_quote[1]
