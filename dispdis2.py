import csv

def aggrCols():
	csvfile=file('simpl.csv','rb')
	fin=csv.reader(csvfile)

	result1=[[],[],[],[],[],[],[],[],[]]
	for line in fin :
		for i in range(9) :
			result1[i].append(line[i])
	print result1

aggrCols()



	
    
  
