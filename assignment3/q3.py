import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)

if(len(sys.argv) == 1):
	prefix = 'ENGG'
elif(len(sys.argv) == 2):
	prefix = sys.argv[1]

query = """
select b.name, string_agg(DISTINCT temp4.code, ' ') from buildings as b join
(select r.within, temp3.code from rooms as r join
(select room_id, temp2.code from meetings as m join
(select c.id, temp1.code from classes c join
(select temp.id, s.code, substring(s.code,1,4) as prefix from subjects s join
(select id, subject_id from courses where term_id = 5196) as temp
on(s.id = temp.subject_id) where substring(s.code,1,4) = %s) as temp1
on(c.course_id = temp1.id)) as temp2
on(m.class_id = temp2.id)) as temp3
on(r.id = temp3.room_id)) as temp4
on(b.id = temp4.within)
group by b.name
;
"""

cur = conn.cursor()
cur.execute(query, [prefix])

for tup in cur.fetchall():
	x,y = tup
	print(x)
	codes = y.split(' ')
	for code in codes:
		result = " "
		result += code
		print(result)

conn.close()
