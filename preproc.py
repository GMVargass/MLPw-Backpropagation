from funcs import *


def selecionaTeste(matriz):
    tam=len(matriz)
    teste=[]
    valida=int(len(matriz)*0.09)
    for x in range(0,valida):
        teste.append(matriz[x])
        del matriz[x]
    return teste

def setTreinamento(matriz,rodada):
    tamGrupo=int((len(matriz))*0.1)
    for x in range(0,(tamGrupo*rodada)):
        matriz[x][(len(matriz[0])-1)]=0
    for y in range( (tamGrupo*rodada) ,(tamGrupo*rodada+tamGrupo)):
        matriz[y][(len(matriz[0])-1)]=1
    for z in range(((tamGrupo*rodada+tamGrupo)),len(matriz) ):
        matriz[z][(len(matriz[0])-1)]=0
    return matriz

def normaliza(matriz):
	maiorMenor=encontraMaiorMenor(matriz)
	normaliza5d=list(range(6))
	normaliza3d=list(range(6))
	normaliza1d=list(range(6))
	fim=len(matriz)
	vetNormalizado=[]
	#print(fim)
	for i in range(0,fim):
		#nesse for sera feita a normalizacao do banco original, com os 6 primeiros atribs, e as 3 medias
		for j in range(0,9):
			matriz[i][j]=(matriz[i][j]-maiorMenor[0][j]) / (maiorMenor[1][j]-maiorMenor[0][j])
			#if (j==8):
			#	matriz[i].append(matriz[i][1])
	#esse for aqui e pra acrescentar algumas coisas ao banco
	for i in range(0,fim):
		if ( (fim-1)>i ):
			#aqui acrescenta a resposta de cada dia, que e o valor maximo do dia seguinte
			matriz[i].append(matriz[i+1][1])
			#aqui ele adiciona um zero, que usarei para dizer se e treinamento ou validacao no k-fold
			matriz[i].append(0)
	#apaga a ultima instancia do banco, pois nao tenho a informacao do dia seguinte dela
	del matriz[fim-1]
	#print(len(matriz))		
	return matriz

