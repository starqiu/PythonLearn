def read_spec_lines(file_name,line1,line2):
	f = open(file_name)
	for index,line in enumerate(f):
		if index == line1:
			print line
		elif index == line2:
			print line
			break
def read_spec_lines_with_linecache(file_name,line1,line2):
	import linecache
	print linecache.getline(file_name,line1)
	print linecache.getline(file_name,line2)
read_spec_lines_with_linecache("week7.py",3,5)