
# lists
a = ['spam', 'eggs', 100, 1234]

print a[0]
print a[3]

print a[-2]


#fibonacci sequence
a, b = 0, 1 # multiple assignment 
while b < 10:
	print b,
	a, b = b, a+b
	
i = 256*256
print 'The value of i is',i
