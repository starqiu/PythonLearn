#!usr/bin/python

def is_pal(name):
	reverse_name = name[::-1]
	if name == reverse_name:
		return True
	else:
		return False
def find_longest_pal_name():
	f = open("names.txt")
	maxLength = 0
	max_length_name =""
	temp_length = 0
	for line in f:
		line = line.strip()
		if is_pal(line):
			temp_length = len(line)
			if temp_length > maxLength :
				maxLength = temp_length
				max_length_name = line
	print max_length_name

def print_hello():
	s = raw_input()
	y = 0
	 
	for i in s:
	    y += 1
	    print y, i

def print_reverse_str_times():
	s1 = raw_input()
	index = 0
	s2 = ''
	 
	while index < len(s1) - 1:
	    if s1[index] > s1[index + 1]:
	        s2 += s1[index]
	    else:
	        s2 = s2 * 2
	         
	    index += 1
	     
	print s2

def convert_str_to_pig_latin(str):
	str_array = str.lower().split()
	for i,s in enumerate(str_array):
		if s[0] in "aeiou":
			str_array[i] = s + "hay"
		elif s.startswith("qu"):
			str_array[i] = s[2:] + "quay"
		else:
			end_index = 0
			for index,ch in enumerate(s[1:]):
				if ch not in "aeiouy":
					end_index = index
				else:
					break
			str_array[i] = s[end_index+1:] +s[:end_index+1]+"ay"
	print ' '.join(str_array)

convert_str_to_pig_latin("Python is intended to be a highly readable language It is designed to have an uncluttered visual layout frequently using English keywords where other languages use punctuation Furthermore Python has a smaller number of syntactic exceptions and special cases than C or Pascal")