import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)

if(len(sys.argv) == 1):
	code = 'COMP1521'
elif(len(sys.argv) == 2):
	code = sys.argv[1]

query = """
select (ct.name || ' ' || temp2.tag || ' is ' || perc || ' full') as info from classtypes as ct join
(select cla.id, cla.type_id, cla.tag, round((count(*) * 100)::numeric / cla.quota, 0)::text||'%%' as perc from classes cla join
(select c.id from courses c join subjects s
on(c.subject_id = s.id)
where substring(s.code,1,8) = %s
and c.term_id = 5199) as temp
on(cla.course_id = temp.id)
join class_enrolments ce
on(cla.id = ce.class_id)
group by cla.id
having round((count(*) * 100)::numeric / cla.quota, 0) < 50) as temp2
on(ct.id = temp2.type_id)
order by ct.name, temp2.tag, temp2.perc
;

"""

cur = conn.cursor()
cur.execute(query, (code,))

for tup in cur.fetchall():
	print(tup[0])

conn.close()
