# -*- coding: utf-8 -*-

import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def diff(a,b):
    ac = a.replace('.','').replace(',','').replace(' ','')
    bc = b.replace('.','').replace(',','').replace(' ','')
    
    if ac!=bc:
        if len(ac) < len(bc):
            temp = bc[:len(ac)]
            res = ac==temp
        elif len(ac) > len(bc):
            temp = ac[:len(bc)]
            res = bc==temp
        else:
        	res = False
    else:
    	res = True

    return res

db = MySQLdb.connect(host="localhost", user="nadia", passwd="1111", db = "outlets")

cur = db.cursor()

cur.execute("SET NAMES UTF8")
cur.execute("SELECT * FROM outlets")

addresses = []
names = []
ids = []

for row in cur.fetchall():
	ids.append(int(row[0]))
	names.append(row[2])
	addresses.append(row[3])

dupes = []
drange = 10
for i in range(len(ids)):
	if i in dupes:
		continue

	for j in range(i+1, min(i+drange, len(ids))):
		if diff(names[i], names[j]):
			dupes.append(ids[j])

			if len(addresses[j]) > len(addresses[i]):
				addresses[i] = addresses[j]

unique = [i for i in ids if i not in dupes]
print unique[1:100]
print 'Number if unique records: ' + str(len(unique))

for i in range(len(unique)):
	insert = "INSERT INTO outlets_clean VALUES (" +  str(i+1) + ", '" + addresses[i] + "')"
	cur.execute(insert)

	cur.execute("SELECT MAX(ID) FROM outlets_clean")
	mxid = cur.fetchall()[0][0]

	nextid = (unique[i+1]-1) if (i < len(unique) - 1) else 20208
	update = "UPDATE outlets SET outlet_clean_id = " + str(mxid) + " WHERE id BETWEEN " + str(unique[i]) + " AND " + str(nextid)
	cur.execute(update)

db.commit()

db.close()