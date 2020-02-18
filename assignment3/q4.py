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
select t.name, String_agg(temp1.main, ' ') from terms as t join
(select (s.code || '(' || temp.counts || ')') as main, temp.id, temp.term_id  from subjects s join
(select c.id, c.subject_id, c.term_id, count(*) as counts from courses c join Course_Enrolments e
on(c.id = e.course_id) group by c.id) as temp
on(s.id = temp.subject_id) where substring(s.code,1,4) = %s
order by main) as temp1
on(t.id = temp1.term_id)
group by t.name
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
