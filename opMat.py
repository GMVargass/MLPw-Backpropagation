

# Calcula as matrizes resultantes da decomposicao de A em L e U.
def DecomposicaoLU(A, L, U):
	n = len(A)
	for j in range(0,n):
		for i in range(0,n):
			if (i <= j ): #matriz triangular superior
			#calculo da matriz L
				if (i == j):#diagonal principal
					L[i][j]=1
				else:
					L[i][j]=0
				# Calculo da matriz U.
				U[i][j] = A[i][j]
				for k in range(0,i-1):
					U[i][j] -= L[i][k] * U[k][j]
				
			
			else: # Matriz triangular inferior.
				# Calculo da matriz L.
				L[i][j] = A[i][j]
				for k in range(0,j-1): 
					L[i][j] -= L[i][k] * U[k][j]
				
				L[i][j] /= U[j][j]
				# Calculo da matriz U.
				U[i][j] = 0


def resolveDecomposicaoLU(n,  m,  L,  U, B):
	
	X = list(range(n))
	Y= list(range(n))
	for i in range(0,n):
		X[i] = list(range(m))
		Y[i] = list(range(m))
	
	for i in range(0,n):
		for j in range(0,m):
			Y[i][j] = B[i][j]
			for k in range(0,i):
				Y[i][j] -= L[i][k]*Y[k][j]

	for i in range((n-1),-1,-1):
		for j in range(0,m):
			X[i][j] = Y[i][j]
			for k in range((i+1),n):
				X[i][j] -= U[i][k]*X[k][j]
			X[i][j] /= U[i][i];

	del Y
	
	return X;

# Calcula o determinante da matriz U (decomposicao LU),que eh dada pela multiplicacao dos elementos da diagonal principal.
def detU( n,  U):
	det = 1.0
	for i in range(0,n): 
		det = det * U[i][i]
	
	return det

# Calcula e retorna a transposta de uma matriz.
def Transposta(original):
	l=len(original)
	c=len(original[0])
	transposta = list(range(c))
	for i in range(0,c):
		transposta[i] = list(range(l))
	for i in range(0,l):
		for j in range(0,c):
			transposta[j][i] = original[i][j]
	return transposta


# Cria a matriz identidade de tamanho [NxN].
def criaIdentidade(n): 
	identidade = list(range(n))
	for i in range(0,n):
		identidade[i] = list(range(n))
	
	for i in range(0,n):
		for j in range(0,n):
			if (i == j):
				identidade[i][j] = 1.0
			
			else: 
				identidade[i][j] = 0.0
	
	return identidade


# Efetua o calculo da matriz resultante da soma de duas matrizes.
def somaMat( matriz1,  matriz2): 	
	resultante = list( range ( len ( matriz1 ) ) ) 
	for i in range(0, len (matriz1) ): 
		resultante[i] = list( range ( len ( matriz1[i] ) ) ) 
		for j in range(0, len (matriz1[i]) ): 
			resultante[i][j] = matriz1[i][j] + matriz2[i][j]
	return resultante


# Efetua a multiplicacao de duas matrizes, retornando uma terceria matriz como resultado.
def multMat(qtdecolunasm2,matriz1,matriz2):
	qtdlinhasM1=len(matriz1)
	qtdecolunasm1=len(matriz1[0])

	matriz3 = list(range(qtdlinhasM1))

	for i in range(0,qtdlinhasM1):
		matriz3[i] =list(range(qtdecolunasm2))

	for i in range(0,qtdlinhasM1):
		for j in range(0,qtdecolunasm2): 
			somaprod = 0.0
			if(qtdecolunasm2==1):
				for k in range(0,qtdecolunasm1):
					somaprod+=(matriz1[i][k] * matriz2[k])
			else:
				for k in range(0,qtdecolunasm1):
					somaprod+=(matriz1[i][k] * matriz2[k][j]) 
				
			matriz3[i][j] = somaprod
	return matriz3


# Efetua a multiplicacao de uma matriz por uma constante, retornando uma nova matriz como resultado.
def multiplicaConstante( matriz1,  constante):
	resultante = list(range ( len(matriz1) ) )
	for i in range(0 , len(matriz1) ):
		resultante[i] = list(range (len(matriz1[0]) ) )
	
	for i in range(0 , len(matriz1) ):
		for j in range(0,len(matriz1[0])):
			resultante[i][j] = matriz1[i][j] * constante
		
	return resultante


def detMatriz(a): 

	n = len(a)
	det = 0

	if (n < 1):  # Error 
		prinf("ERRO: Calculo do Determinante de uma matriz com numero de linhas menor que 1!\n")
		exit(0)
	elif (n == 1):  
		det = a[0][0]
	elif(n == 2):
		det = a[0][0] * a[1][1] - a[1][0] * a[0][1]
	else:
		det = 0
		for jj in range(0,n): 
			m = list(range((n-1)))
			for i in range(0,(n-1)): 
				m[i] = list(range((n-1)))
			
			for i in range(0,n):
				j2 = 0
				for j in range(0,n):
					if (j != jj):
						m[i-1][j2] = a[i][j]
						j2+=1
			det += math.pow(-1.0,jj+2.0) * a[0][jj] * detMatriz(m)
			del m
		
	return det


def tadMatriz_Singular( a,  n):
	return true



