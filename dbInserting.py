import sqlite3

fn = "Jane"
ln = "Doe"
ad = "21 Smith Street"
sub="Karori"
pc="0000"
pho = "021 667 8934"
em="janedoe@hotmail.com"
bday="12/04/2000"
gender="Other"
bio = "Bio goes here"


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
db_insert(fn, ln, ad, sub, pc, pho, em, bday, gender, bio)


