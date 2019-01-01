import sqlite3



def connection(sql):
    conn =sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    fields = conn.execute('select * from memberTable')
    f = [description[0] for description in fields.description]
    print(f)
    cur.execute(sql)
    result = cur.fetchall()
    conn.commit()
    conn.close()
    if len(result) == 0:
        result = (("No value found", ), )
    return result


def wide_search(s):
    sql = 'select * from memberTable where lastName like "%{0}%" ' \
          'or address like "%{0}%" or suburb like "%{0}%" '.format(s)
    return sql


def id_search(id):
    sql = 'select * from memberTable where memberID = {}'.format(id)
    return sql


def print_result(r):
    print(type(r))
    for x in r:
        for y in x:
            print(y)


cont = ""
while cont == "":
    my_search=input("Please enter for wide search: ")
    result= connection(wide_search(my_search))
    print_result(result)
    my_search=input("Please enter for id search: ")
    result = connection(id_search(my_search))
    print_result(result)
    cont = input("Please press any key to exit or <Enter> to continue: ")
