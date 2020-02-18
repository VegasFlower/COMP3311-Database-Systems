import sys
import psycopg2


try:
	conn = psycopg2.connect("dbname=a3")

except Exception as e:
	print("Cannot connect to a3 database...")
	sys.exit(1)

nums = 0

if(len(sys.argv) == 1):
	courses = ('COMP1511','MATH1131')
	nums = 2
elif(len(sys.argv) == 2):
	courses = (sys.argv[1],'zxcc')
	nums = 1
elif(len(sys.argv) == 3):
	courses = (sys.argv[1],sys.argv[2])
	nums = 2
elif(len(sys.argv) == 4):
	courses = (sys.argv[1], sys.argv[2], sys.argv[3])
	nums = 3


query1="""
select s.code, cs.id, ct.name, ms.day, ms.start_time, ms.end_time from courses c
join subjects s on(c.subject_id = s.id)
join classes cs on(c.id = cs.course_id)
join classtypes ct on(cs.type_id = ct.id)
join meetings ms on(cs.id = ms.class_id)

where c.term_id = 5199
and s.code in %s

order by s.code, cs.id, ct.name, ms.day, ms.start_time
;
"""
cur = conn.cursor()
cur.execute(query1,[courses])

total = []
total_list = []

for a in cur.fetchall():
	total.append(a)

query2 = """
select code, name, count(DISTINCT id) from
(select s.code, cs.id, ct.name, ms.day, ms.start_time, ms.end_time from courses c
join subjects s on(c.subject_id = s.id)
join classes cs on(c.id = cs.course_id)
join classtypes ct on(cs.type_id = ct.id)
join meetings ms on(cs.id = ms.class_id)
where c.term_id = 5199
and s.code in %s
order by s.code, cs.id, ct.name, ms.day, ms.start_time) temp
group by code, name
order by count(DISTINCT id)
;
"""

cur = conn.cursor()
cur.execute(query2, [courses])

visited = []
stack = []

def same_class(b):
	for a in stack:
		if(a[0] == b[0] and a[2] == b[2]):
			if(a[1] != b[1]):
				return False
			if(a[1] == b[1]):
				if(a[3]==b[3] and a[4] == b[4] and a[5] == b[5]):
					return False
				else:
					return True
	return False

def check_clash(b):
	for a in stack:
		if(a[0] == b[0] and a[2] == b[2]):
			return False
	for a in stack:
		if(a[3] == b[3]):
			if(a[4] <= b[4]):
				if(a[5] > b[4]):
					return False
			else:
				if(b[5] > a[4]):
					return False
	return True

def check(a,b):
	if(a[3] == b[3]):
		if(a[4] <= b[4]):
			if(a[5] > b[4]):
				return False
		else:
			if(b[5] > a[4]):
				return False
	return True

det_list = []

for i in cur.fetchall():
	det_list.append(i)

for a in det_list:
	if(a[2] == 1):
		for b in total:
			if(b[0] == a[0] and b[2] == a[1]):
				visited.append(b)
				stack.append(b)
			else:
				total_list.append(b)

for i in stack:
	for j in stack:
		if(i[1] != j[1]):
			if(check(i,j) == False):
				print("????")
				conn.close
				sys.exit(1)



for tup in total_list:
	if(len(stack) == 0):
		visited.append(tup)
		stack.append(tup)
	elif(tup not in visited):
		if(same_class(tup) == True):
			visited.append(tup)
			stack.append(tup)
		else:
			if(check_clash(tup) == True):
				visited.append(tup)
				stack.append(tup)
		visited.append(tup)

def sortby(val):
	return val[3]

def sort(val):
	return val[4]

stack.sort(key = sort)
stack.sort(key = sortby, reverse = True)

def getTime(a,b):
	hour = (b // 100) - (a // 100)
	mins = ((b % 100) - (a % 100)) / 60
	hours = hour + mins

	return hours



total_time = 0
days = []

for tup in stack:
	if(tup[3] not in days):
		days.append(tup[3])

total_time += len(days) * 2

for day in days:
	min_time = 2500
	max_time = 0
	for i in stack:
		if(i[3] == day):
			if(i[4] < min_time):
				min_time = i[4]
			if(i[5] > max_time):
				max_time = i[5]
	total_time += getTime(min_time, max_time)

print("Total hours: " + str(total_time))



s = 0
for tup in stack:
	if(tup[3] == 'Mon'):
		s =1
if(s == 1):
	sb = '  Mon'
	for i in stack:
		if(i[3] == 'Mon'):
			sb += '\n' + '    ' + i[0] + ' ' + i[2] + ': ' + str(i[4]) +'-'+str(i[5])
	print(sb)
s = 0
for tup in stack:
	if(tup[3] == 'Tue'):
		s =1
if(s == 1):
	sb = '  Tue'
	for i in stack:
		if(i[3] == 'Tue'):
			sb += '\n' + '    ' + i[0] + ' ' + i[2] + ': ' + str(i[4]) +'-'+str(i[5])
	print(sb)

s = 0
for tup in stack:
	if(tup[3] == 'Wed'):
		s =1
if(s == 1):
	sb = '  Wed'
	for i in stack:
		if(i[3] == 'Wed'):
			sb += '\n' + '    ' + i[0] + ' ' + i[2] + ': ' + str(i[4]) +'-'+str(i[5])
	print(sb)
s = 0
for tup in stack:
	if(tup[3] == 'Thu'):
		s =1
if(s == 1):
	sb = '  Thu'
	for i in stack:
		if(i[3] == 'Thu'):
			sb += '\n' + '    ' + i[0] + ' ' + i[2] + ': ' + str(i[4]) +'-'+str(i[5])
	print(sb)
s = 0
for tup in stack:
	if(tup[3] == 'Fri'):
		s =1
if(s == 1):
	sb = '  Fri'
	for i in stack:
		if(i[3] == 'Fri'):
			sb += '\n' + '    ' + i[0] + ' ' + i[2] + ': ' + str(i[4]) +'-'+str(i[5])
	print(sb)


conn.close()
