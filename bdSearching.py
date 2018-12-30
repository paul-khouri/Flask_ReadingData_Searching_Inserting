import sqlite3

# connect
def db_Search(s):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where lastName like "%{0}%" ' \
          'or address like "%{0}%" or suburb like "%{0}%" '.format(s)
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    for x in result:
        print(x)

my_search=input("Please enter your search query: ")
db_Search(my_search)
