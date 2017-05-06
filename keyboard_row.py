import time

#Keyboard row

def findLetterInRows(letter,rows):
	for row in rows:
		print "<<------------------>>"		
		if findLetterInRow(letter,row):
			return row
		
		#if a letter is found in a row, search only that row, and advance to the next letter
		
		
		

def findLetterInRow(letter,row):
		
	print "Letter:{0}".format(letter)
	print "Row:{0}".format(row)
		
	for rowletter in row:
		print 'Rowletter: {0} <-> Letter: {1}'.format(rowletter,letter)	
			
		if (str(rowletter.lower()) == str(letter.lower())):
			print "match"
			time.sleep(.2)
			return 1
		else:
			print "no match"
			return 0

def findWordInRow(word,row):
	for letter in word:
		if findLetterInrRow(letter,row): 
		#if I find a letter in this row, 
		#re-search the row for all the other letters.
			print letter		
		
rows = [["q","w","e","r","t","y","u","i","o","p"],["a","s","d","f","g","h","j","k","l"],["z","x","c","v","b","n","m"]]

input = ["Hello", "Alaska", "Dad", "Peace"]

output = ""
outlist = []

for word in input:
	for row in rows:
		findWordInRow(word,rows)