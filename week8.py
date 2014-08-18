def exam2():
	a = [1, 2, 3]
	b = a[:]
	b[1] = 4
	print a[1]
ops_g =['+','-','*','/','**']
nums_g = ['2','3','4','5']

def exam3(ops,nums,res_str):
	if len(nums) == 1:	
		res_str += 	nums[0]
		#print res_str
		if eval(res_str) == 28:
			print res_str
	else:
		for num in nums :
			for op in ops:
				exam3([o for o in ops if o!=op],[n for n in nums if n!=num],res_str + num + op)
			
	

def is_pal(name):
	reverse_name = name[::-1]
	if name == reverse_name:
		return True
	else:
		return False

def exam4():
	num_2bit_pal = [x for x in range(10,100) if x%10 == x/10]
	num_3bit_pal = [x for x in range(100,1000) if x%10 == x/100]
	print num_2bit_pal 
	print num_3bit_pal 
	plus_res = 0
	for n2 in num_2bit_pal:
		for n3 in num_3bit_pal:
			plus_res = n2 + n3
			if (plus_res/1000 >0) and is_pal(str(plus_res)):
				print n2," ",n3," ",plus_res

def exam5():
	list1 = [1, 2, 3]
	list2 = list1
	list3 = list2
	list1.remove(1)
	print list3[1]

def  shift_left(lst):
	first = lst[0]
	for i in range(len(lst)-1):
		lst[i]=lst[i+1]
	lst[-1]=first
	return lst

#exam3(ops_g,nums_g,"")
print shift_left(['a','b','c','d'])