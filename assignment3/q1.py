import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)


query = """
	select s.code as Course_Code, temp.perc as perc
	from subjects s
	join (select c.id, c.subject_id as subject_id, round((count(*) * 100)::numeric / c.quota, 0)::text||'%' as perc from courses c
		  join Course_Enrolments ce on(ce.course_id=c.id)
		  join terms t on(c.term_id=t.id)
		  where c.quota > 50
		  and t.name = '19T3'
		  group by c.id having count(*) > c.quota) as temp on(s.id=temp.subject_id)
	order by s.code;
"""

cur = conn.cursor()
cur.execute(query)

for tup in cur.fetchall():
	x,y = tup
	print(x,y)

conn.close()
