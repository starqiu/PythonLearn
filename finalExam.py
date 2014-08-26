def classifyWords():
	f = open("words.dic")
	dic = {}
	key = ""
	for word in f:
		word = word.replace("\n","")
		key = "".join(sorted(word))
		if key in dic:
			dic[key].append(word)
		else:
			dic[key] = [word]
	classifiedWordList =[]
	for value in dic.values():
		classifiedWordList.append((len(value),value[0],value))
	classifiedWordList.sort(reverse = True)
	resList = [x[2] for x in classifiedWordList]
	print resList

		
def findErr():
	x = int(raw_input('Input a Positive number: '))
	if x< 0:
		print "you input a negative number,please input a Positive number"
	else:
		low = 0
		high = x
		ans = (low + high) / 2
		 
		while ans**2 != x:
		    if ans**2 < x:
		        low = ans + 1
		    else:
		        high = ans - 1
		    ans = (low + high) / 2
		 
		print ans

def guessWord(word):
	import re
	subStr = ""
	rule =r"[a-z]"
	ch = raw_input("Enter a letter in word "+re.sub(rule,"*",word)+": ")
	while ch != "":
		if ch in subStr:
			print ch + "is already in the word"
		else:
			if ch in word:
				subStr += ch
				rule = r"[^"+subStr+"]"
				print rule
				ch = raw_input("Enter a letter in word "+re.sub(rule,"*",word)+": ")
			else:
				print "The word is" + word+". You missed 1 time(s)."
				ch =""

classifyWords()	
#guessWord(raw_input("Input a word:\n"))
#findErr()

