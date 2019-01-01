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

def db_search_id(id):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where memberID = {} '.format(id)
    cur.execute(sql)
    member = cur.fetchall()
    sql = 'select * from results where memberID = {} '.format(id)
    cur.execute(sql)
    results = cur.fetchall()
    conn.close()
    for x in member:
        print(x)
    for x in results:
        print(x)


# delete given an ID
def db_delete_id(id):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql ="delete from memberTable where memberID = {}".format(id)
    cur.execute(sql)
    conn.commit()
    sql ="delete from results where memberID = {}".format(id)
    cur.execute(sql)
    conn.commit()
    conn.close()



my_search_id=input("Please enter an ID number: ")
db_search_id(my_search_id)
db_delete_id(my_search_id)

#my_search=input("Please enter your search query: ")
#db_Search(my_search)


