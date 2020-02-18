import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)

if(len(sys.argv) == 1):
	term = '19T1'
elif(len(sys.argv) == 2):
	term = sys.argv[1]

query1="""
select id from rooms
where code like 'K-%'
group by id
order by id
;
"""
cur = conn.cursor()
cur.execute(query1)

thisdict = {}
total = 0

for a in cur.fetchall():
	x = a[0]
	x = int(x)
	thisdict[x] = 0
	total+=1
print(total)

query2 = """
select start_time, end_time, room_id, weeks_binary 
from meetings m
join rooms r on(m.room_id = r.id)
join classes c on(m.class_id = c.id)
join courses cs on(c.course_id = cs.id)
join terms t on(cs.term_id = t.id)
where t.name = %s
and r.code like 'K-%%'
;
"""

cur = conn.cursor()
cur.execute(query2, [term])

for tup in cur.fetchall():
	a,b,c,d = tup
	hours_4 = b - a

	hour = (b // 100) - (a // 100)
	mins = ((b % 100) - (a % 100)) / 60

	hours = hour + mins
	d = d[:-1]
	d = d.replace('0', '')
	hours = hours * len(d)

	c = int(c)
	temp = thisdict[c]
	new = temp + hours
	thisdict[c] = new

nums = 0

for i in thisdict:
	j = thisdict[i]
	if((j/10) < 20):
		nums+=1
#print(nums)
print("{:.1%}".format(nums/total))

conn.close()
