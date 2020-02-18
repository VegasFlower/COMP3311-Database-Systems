import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)



query1 = """
select id, weeks from meetings
"""

query2 = """
update meetings set weeks_binary = %s where id = %s;
"""

cur = conn.cursor()
cur.execute(query1)

for tup in cur.fetchall():
	x,y = tup
	if(y.find('N') != -1 or y.find('<') != -1):
		result = '00000000000'
		tupId = x
		cur.execute(query2,(result, tupId))
	else:
		thelist = []
		tokens = y.split(',')
		for token in tokens:
			if '-' in token:
				new_tokens = token.split('-')
				a = int(new_tokens[0])
				b = int(new_tokens[1])
				for i in range (a, b+1):
					thelist.append(i)
			else:
				thelist.append(int(token))
		result = ''
		if 1 in thelist:
			result += '1'
		else:
			result += '0'
		if 2 in thelist:
			result += '1'
		else:
			result += '0'
		if 3 in thelist:
			result += '1'
		else:
			result += '0'

		if 4 in thelist:
			result += '1'
		else:
			result += '0'
		if 5 in thelist:
			result += '1'
		else:
			result += '0'
		if 6 in thelist:
			result += '1'
		else:
			result += '0'
		if 7 in thelist:
			result += '1'
		else:
			result += '0'
		if 8 in thelist:
			result += '1'
		else:
			result += '0'
		if 9 in thelist:
			result += '1'
		else:
			result += '0'
		if 10 in thelist:
			result += '1'
		else:
			result += '0'
		if 11 in thelist:
			result += '1'
		else:
			result += '0'
	
		tupId = x

		cur.execute(query2, (result, tupId))


conn.commit()
conn.close()
