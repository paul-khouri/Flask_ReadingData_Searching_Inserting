import datetime


def string_to_date(s):
    temp=s.split("-")
    new_date = datetime.datetime(int(temp[0]), int(temp[1]), int(temp[2]))
    return new_date



    print(temp)

mydate="2017-09-11"
mydate = string_to_date(mydate)
print(mydate)
print(type(mydate))
print(mydate.strftime("%Y-%m-%d"))
