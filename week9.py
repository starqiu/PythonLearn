def exam6():
	d1 = {}
	d1[2] = 10
	d1['2'] = 20
	print d1[2]
	d2 = {}
	d2[2] = d1
	print d2
	d2['2'] = d2
	print d1
	print d2 
	print d2['2']['2']['2']['2'][2][2]

def exam7():
	d = { }
	d['susan'] = 50
	d['jim'] = 45
	d['joan'] = 54
	d['susan'] = 51
	d['john'] = 55
	print len(d)

exam7()