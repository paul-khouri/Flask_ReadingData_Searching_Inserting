from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

def db_Search(s):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where lastName like "%{0}%" ' \
          'or address like "%{0}%" or suburb like "%{0}%" '.format(s)
    cur.execute(sql)
    result = cur.fetchall()
    conn.close()
    return result

def db_insert(fn, ln, ad, sub, pc, pho, em, bday, gender, bio):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'INSERT INTO memberTable (firstName, lastName, address, suburb, postcode, ' \
          'phoneNumber, email, birthDate, gender, bio) ' \
          'Values( "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(fn,ln,ad, sub, pc, pho, em, bday, gender, bio)
    print(sql)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "Message"


def db_search_id(id):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where memberID = {} '.format(id)
    cur.execute(sql)
    member = cur.fetchone()
    if member is None:
        member_message = "No member with this ID has been found"
    else:
        member_message= "The member {} {} has been found and can now be deleted".format(member[1], member[2])
    sql = 'select * from results where memberID = {} '.format(id)
    cur.execute(sql)
    results = cur.fetchall()
    if len(results) == 0:
        results_message = "There are no competition entries to be deleted"
    else:
        results_message = "The are {} competition entries that will also be deleted ".format(len(results))
    conn.close()
    return member_message,results_message

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


@app.route('/')
def main_index():
    query_f_k = 'select memberTable.firstName, memberTable.lastName from memberTable where gender = "Female" and suburb = "Karori";'
    query_vod = 'select memberTable.firstName, memberTable.lastName, memberTable.phoneNumber from memberTable where phoneNumber like "%021%";'
    query_event = ' select event, strftime("%d-%m-%Y", eventDate) as "Event Date" ' \
                  'from events where eventDate between "2018-02-21" and "2018-31-12" order by eventDate asc;'
    query_results = 'select events.event, memberTable.firstName, memberTable.lastName, ' \
                    'results.result, results.eventType, strftime("%d-%m-%Y", eventDate) as "Event Date" ' \
                    'from events ' \
                    'join results ' \
                    'on events.eventID=results.eventID ' \
                    'join memberTable ' \
                    'on results.memberID=memberTable.memberID ' \
                    'where events.eventDate>="2017-08-10" order by events.eventDate asc;'
    query_underage = 'select memberTable.firstName, memberTable.lastName, strftime("%d-%m-%Y", memberTable.birthDate) as "Birthdate", ' \
                     'date("now")-memberTable.birthDate as "Age", memberTable.bio ' \
                     'from memberTable where Age<18 order by birthDate asc;'

    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    cur.execute(query_f_k)
    f_k = cur.fetchall()

    cur.execute(query_vod)
    vod = cur.fetchall()

    cur.execute(query_event)
    event = cur.fetchall()

    cur.execute(query_results)
    results = cur.fetchall()

    cur.execute(query_underage)
    underage = cur.fetchall()

    conn.close()

    return render_template("index.html", f_k=f_k, vod=vod, event=event, results=results, underage=underage)


@app.route('/search', methods=['GET', 'POST'])
def my_search():
    if request.method == 'POST':
        print("from post")
        s = request.form['mysearch']
        result = db_Search(s)
        return render_template("search.html", result = result)
    elif request.method == 'GET':
        print("from get")
        return render_template("search.html")


@app.route('/insert')
def my_insert():
    return render_template("insert.html")


@app.route('/insertcomplete', methods=['POST'])
def insert_complete():
    fn = request.form['fn']
    ln = request.form['ln']
    ad = request.form['ad']
    sub = request.form['sub']
    pc = request.form['pc']
    pho = request.form['pho']
    em = request.form['em']
    bday = request.form['bday']
    gender = request.form['gender']
    bio = request.form['bio']
    msg = db_insert(fn, ln, ad, sub, pc, pho, em, bday, gender, bio)
    q='SELECT * FROM memberTable ORDER BY memberID DESC LIMIT 1'
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    cur.execute(q)
    result = cur.fetchone()
    print(result)
    return render_template("insertcomplete.html", msg=msg, result=result)


@app.route('/admin')
def my_admin():
    return render_template("admin.html")


temp = None
@app.route('/delete' , methods=['GET', 'POST'])
def my_delete_id():
    if request.method == 'GET':
        return render_template("delete_id.html")
    elif request.method == 'POST':
        global temp
        if temp is None:
            s = request.form['my_delete_id']
            result = db_search_id(s)
            print(result)
            return render_template("delete_id.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)