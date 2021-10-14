x = input("Enter a number ")
x = int (x)
i = 1
c = 0 
while i < x : 
	if x % i == 0 :
		c = c + i 
	i = i + 1

if c == x:
	print ("el numero %s es perfecte" % (x))
else: 
	print ("el numero %s no es perfecte" % (x))
