from flask import Flask, render_template, request, session
from mainform import MainForm
import sqlite3
import datetime
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def string_to_date(s):
    temp=s.split("-")
    new_date = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))
    return new_date

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


def db_update(id, fn, ln, ad, sub, pc, pho, em, bday, gender, bio):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql ='update memberTable set firstName = "{}", lastName =  "{}" , address="{}" , suburb="{}" , ' \
         'postcode = "{}", phoneNumber = "{}" , email= "{}", birthDate = "{}" ,' \
         'gender = "{}", bio = "{}" where memberID = "{}" '.format(fn, ln, ad, sub, pc, pho, em, bday, gender, bio,id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return None


def db_get_all_id(id):
    if id == "":
        return None
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where memberID = {} '.format(id)
    cur.execute(sql)
    member = cur.fetchone()
    conn.close()
    return member

def db_search_id(id):
    conn = sqlite3.connect('memberTable.sqlite')
    cur = conn.cursor()
    sql = 'select * from memberTable where memberID = {} '.format(id)
    cur.execute(sql)
    member = cur.fetchone()
    if member is None:
        return None
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
    return "The member with memberId {}, has been deleted, along <br> with any competition results".format(id)


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



@app.route('/delete' , methods=['GET', 'POST'])
def my_delete_id():
    if request.method == 'GET':
        return render_template("delete_id.html")
    elif request.method == 'POST':
            s = request.form['my_delete_id']
            session['idkey'] = s
            result = db_search_id(s)
            if result is None:
                result=("No member with this ID has been found",)
                return render_template("delete_id.html", result=result)
            else:
                print("Have accessed confirm delete")
                return render_template("confirm_delete.html",  result=result)



@app.route('/deleteconfirmed', methods=['POST'])
def delete_confirmed():
    myvar = session.get('idkey', None)
    message = db_delete_id(myvar)
    return render_template("finalised_delete.html",  msg=message)


@app.route('/update_start', methods=['GET', 'POST'])
def update_start():
    if request.method == 'GET':
        return render_template("update_start.html")
    elif request.method == 'POST':
            s = request.form["my_update_id"]
            session['id'] = s
            result = db_get_all_id(s)
            if result is None:
                result="No member with this ID has been found"
                return render_template("update_start.html", result=result)
            else:
                result = db_get_all_id(s)
                print(result)
                myform = MainForm(csrf_enabled=False)
                myform.firstname.data = result[1]
                myform.lastname.data = result[2]
                myform.address.data = result[3]
                myform.suburb.data = result[4]
                myform.postcode.data = result[5]
                myform.phoneNumber.data = result[6]
                myform.email.data = result[7]
                myform.birthdate.data = string_to_date(result[8])
                myform.gender.data = result[9]
                myform.bio.data = result[10]
                return render_template("update.html", form=myform)


@app.route('/update' , methods=['POST'])
def update():
    myList=[]
    myvar = session.get('id', None)
    myList.append(myvar)
    form = request.form
    for x, y in form.items():
        myList.append(y)
        print("{} {}".format(x,y))
    print(','.join(map(str,myList) ) )
    db_update( myList[0],myList[1],myList[2],myList[3],myList[4],myList[5],myList[6],myList[7],myList[8],myList[9],myList[10])
    return render_template("update_end.html",  form=form)


if __name__ == '__main__':
    app.run(debug=True)