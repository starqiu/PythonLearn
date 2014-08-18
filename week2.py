#! /usr/bin/env python

def bmi(weight,height):
	return weight/(height**2)
def balance(year):
	res =0.0
	for i in range(1,year+1):
		res += (res + 1000)*(1+0.047)
	return res
def printTime(seconds):
	h = seconds /(60*60)
	m = (seconds % (60*60))/60
	s = (seconds %(60*60))%60
	print h," ", m," ",s
def getDegree(a,b,c):
	import math
	temp = float((c**2-a**2-b**2)/(2*a*b))
	print (math.acos(temp))*180/(math.pi)

x = 6
while(x>0):
	#w = float(raw_input())
	#h = float(raw_input())
	#print bmi(w,h)
	#print balance(10)
	#printTime(int(raw_input()))
	#from datetime import *
	#import time
	#print 'date.today():', date.today() 
	a = float(raw_input())
	b = float(raw_input())
	c = float(raw_input())
	getDegree(a,b,c)
	x = x -1