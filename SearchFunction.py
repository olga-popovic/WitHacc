import csv
import math

#string metric
def MatchScore(text, textlist):
	bestScore = 0
	bestWord = ""
	for word in textlist:
		score = 0
		maxLen = len(word)
		if len(text) < maxLen:
			maxLen = len(text)
		for i in range(0,maxLen):
			for j in range(0,len(text) - i + 1):
				#print(i, j, text[j:j+i])
				if text[j:j+i].lower() in word.lower():
					score += i*math.exp(i)
				#else:
					#score -= i
		score = score/((abs(len(text) - len(word)))+len(text)/len(word))
		if score > bestScore:
			bestScore = score
			bestWord = word
		#print(text,"~~~~ =>",word,"=",score)
	if bestScore < 15:
		return None
	else:
		#print(text,"~~~~>",bestWord,"=",bestScore)
		return bestWord

wordlist = []
with open('health_centres.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		wordlist.append((row[4])[2:-1])
#word = "Hello"
#print(wordlist)
#testlist = ["Hello","Prince","Hospital","Health"]
correctlist = ["Randwick", "Sydney", "Kensington","Ultimo","Darlington"]
testlist = ["Rndwick","Sybney","Kensimgton","Uktimo","Barlington"]
testlist += ["rendwich","sadkey","kinsongten","ultimate","duhlangtin"]
testlist += ["raaandwhich","sidknee","kennsanggtonne","uhlteamo","dahrlinghtonne","hello","thisdoesntmakeanysense"]
testlist += ["a","no","notaword","noreturn","iq3jeio2j3","helpme","endme","yeetdabyeet"]
for word in testlist:
	res = MatchScore(word, wordlist)
	if res == None:
		print("No results for '"+word+"'")
	else:
		print("Closest to '"+word+"'is",res)
	#MatchScore(word,wordlist)