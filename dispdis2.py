import csv
csvfile1=file('simpl.csv','rb')
fin1=csv.reader(csvfile1)

label_dict={'back.':0,'buffer_overflow.':1,'ftp_write.':2,'guess_passwd.':3,'imap.':4,'ipsweep.':5,'land.':6,'loadmodule.':7,
       'multihop.':8,'neptune.':9,'nmap.':10,'normal.':11,'perl.':12,'phf.':13,'pod.':14,'portsweep.':15,'rootkit.':16,
       'satan.':17,'smurf.':18,'spy.':19,'teardrop.':20,'warezclient.':21,'warezmaster.':22}

line1=input("please input num1:")
line2=input("please input num2:")

list1=[]
list2=[]
def read_spec_lines(line1,line2):
    csvfile=file('dispresult.csv','rb')
    fin=csv.reader(csvfile)    
    global list1
    global list2
    for index,line in enumerate(fin):
        if index==line1:
                list1=line
                        
        elif index==line2:
                list2=line
                break

read_spec_lines(line1,line2)

print "the list1 is:",list1
print
print "the list2 is:",list2
print

result2=[[],[],[],[],[],[],[],[],[],[]]
for line in fin1:
    for i in range(len(line)):
        result2[i].append(line[i])

#print result2

#init temp row ,for store each row
temp_row=[0 for i in range(23)]
#print temp_row

result3 = []
for row_index in range(9):
	for col_index,col in enumerate(result2[row_index]):
		#print "list1[row_index] ",list1[row_index]
		if list1[row_index] == col :
			label = result2[9][col_index]
			#print label
			label_index = label_dict[label]
			#print label_index
			#print temp_row[label_index]
			temp_row[label_index] += 1
			#print temp_row[label_index]
	#print temp_row
	result3.append(temp_row)
	temp_row=[0 for i in range(23)]
print result3