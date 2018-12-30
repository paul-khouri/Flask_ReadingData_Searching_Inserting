import sqlite3


query_f_k = 'select memberTable.firstName, memberTable.lastName from memberTable where gender = "Female" and suburb = "Karori";'
query_vod ='select memberTable.firstName, memberTable.lastName, memberTable.phoneNumber from memberTable where phoneNumber like "%021%";'
query_event =' select event, strftime("%d-%m-%Y", eventDate) as "Event Date" ' \
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
f_k =cur.fetchall()
for x in f_k:
    for y in x:
        print("{} ".format(y), end="")
    print()

cur.execute(query_vod)
vod=cur.fetchall()
for x in vod:
    for y in x:
        print("{} ".format(y), end="")
    print()

cur.execute(query_event)
vod=cur.fetchall()
for x in vod:
    for y in x:
        print("{} ".format(y), end="")
    print()

cur.execute(query_results)
vod=cur.fetchall()
for x in vod:
    for y in x:
        print("{} ".format(y), end="")
    print()

cur.execute(query_underage)
vod=cur.fetchall()
for x in vod:
    for y in x:
        print("{} ".format(y), end="")
    print()

conn.close()

