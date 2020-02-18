import sys
import psycopg2




try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)

if(len(sys.argv) == 1):
	number = 2
elif(len(sys.argv) == 2):
	if(int(sys.argv[1]) < 2 or int(sys.argv[1]) > 10):
		print("Please enter integer between 2 ad 10")
		sys.exit(1)
	else:
		number = sys.argv[1]

query = """
select r.code_num, string_agg(r.code, ' ') from
(select substring(s.code, '[0-9]+') as code_num, left(s.code, 4) as code from subjects s
join (select substring(code, '[0-9]+') as codes, count(*) as counts from subjects group by codes having count(*) = %s) as temp
on (substring(s.code, '[0-9]+') = temp.codes) order by code) as r
group by r.code_num
order by r.code_num
;
"""

cur = conn.cursor()
cur.execute(query, [number])

for tup in cur.fetchall():
	x,y = tup
	result = x + ': ' + y
	print(result)

conn.close()
