import sqlite3


class sqlight:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def save_file(self, coin_name, price, link, ticket, change_percent, sign):
        with self.connection:
            return self.cursor.execute('INSERT INTO `coins` (`name`, `price`, `link`, `ticket`, `change percent`, `sign`) VALUES(?,?,?,?,?,?)', (coin_name, price, link, ticket, change_percent, sign))


    def delete(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM `coins`')

    def get_price(self, coin_name):
        with self.connection:
            price = self.cursor.execute('SELECT `price` FROM `coins` WHERE `name` = ?', (coin_name, )).fetchone()
            return price



    def close(self):
        self.connection.close()