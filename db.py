import sqlite3

def qry_all_students(qry_id):
	con = sqlite3.connect('test.db')
	cursor = con.cursor()
	cursor.execute("select * from student where id=?",(qry_id,))
	rows = cursor.fetchall()
	for r in rows:
		print r

	print ""
	
	cursor.execute("select * from student ")
	rows = cursor.fetchall()
	for r in rows:
		print r


qry_all_students("SA123")