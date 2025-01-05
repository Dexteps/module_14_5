import sqlite3
def initiate_db():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(
        f'''CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL) '''
    )
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL)'''
    )
    connect.commit()
    connect.close()


def get_all_products(name='database.db'):
    connect = sqlite3.connect(name)
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Products')
    res = cursor.fetchall()
    connect.close()
    return res



def add_db(title, price, description=''):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    check = cursor.execute(f'SELECT * FROM Products WHERE title=?', (f'{title}',))
    if check.fetchone() is None:
        cursor.execute(
            f'''INSERT INTO Products(title, description, price) VALUES('{title}','{price}','{description}')'''
        )
    connect.commit()
    connect.close()

def add_user(username, email, age):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute(f'''INSERT INTO Users(username, email, age, balance) VALUES('{username}', '{email}', '{age}', '1000')''')
    connect.commit()
    connect.close()

def is_included(username):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Users WHERE username=?', (f'{username}',))
    res = cursor.fetchone()
    connect.commit()
    connect.close()
    return res is not None



if __name__ == '__main__':
    initiate_db()





