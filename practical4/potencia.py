x = input("Escriu la base ")
y = input("Escriu l'exponent ")
x = int (x)
y = int (y)
n = 1
i = 0
while i < y:
	n = n * x
	i = i + 1
print ("El resultat de la potencia es %s " % (n))
