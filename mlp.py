import random 
import math
from funcs import *
from opMat import *
#from psopy import *
from preproc import *
import copy

#https://wiki.python.org.br/ProgramacaoOrientadaObjetoPython
#http://www.devfuria.com.br/python/programacao-orientada-objetos/
L=[]
U=[]
B=[]

class Neuronio(object):
	def init(self,qtde):
		self.qtde_W=qtde
	def setValores(self,numero):	
		self.w =list(xrange(numero))
		self.dw=list(xrange(numero))
		self.bias=-1
		self.dbias=0
		self.delta=0
		self.erro=0
		self.saida=1
		

class Rna(object):
	def setValores(self,numCamadas,neuroCamada,entradas):
		self.entrada=entradas
		self.nCamadas=numCamadas
		self.neuroCamada=neuroCamada
		self.neuro=list(xrange(numCamadas))
		self.erroMediaTreino=0
	 	self.erroFinal=0
		self.vetNeuroCamada=[]
		self.momentum=-1
		self.taxaAprendizado=-1

def inicializaPesos(vet,numcamadas,numNeuro):
	#for i in xrange(0,numcamadas):
	for j in xrange(0,numNeuro):
		vet.w[j]=random.random()
  		vet.dw[j]=0
	return vet	

def inicializaRede(qtdNeuroCam,entradas):
	#rede= Rna.setValores(qtdeCaadas,qtdNeuroCam,entradas)
	qtdeCamadas=len(qtdNeuroCam)
	rede=object.__new__(Rna)
	rede.setValores(qtdeCamadas,qtdNeuroCam,entradas)
	for i in xrange(0,qtdeCamadas):
		#vetor de controle, com a quantidade de camadas, em cada posicao(camada) tem a quantidade de neurorios naquela camada.
		rede.vetNeuroCamada.append(qtdNeuroCam[i])
		#pega cada posicao do vetor neuro e cria outro vetor, tornando assim uma matriz 
		rede.neuro[i]=list(xrange(qtdNeuroCam[i]))
		for j in xrange(0,rede.vetNeuroCamada[i]):
			#pega cada posicao da matriz neuronio e torna ela um objeto do tipo neuronio
			rede.neuro[i][j]=object.__new__(Neuronio)
			if(i==0):
				rede.neuro[i][j].init(entradas)
				rede.neuro[i][j].setValores(entradas)
				rede.neuro[i][j]=inicializaPesos(rede.neuro[i][j],qtdeCamadas,entradas)
			else:
				rede.neuro[i][j].init(qtdNeuroCam[i-1])
				rede.neuro[i][j].setValores(qtdNeuroCam[i-1])	
	  			rede.neuro[i][j]=inicializaPesos(rede.neuro[i][j],qtdeCamadas,qtdNeuroCam[i-1])
		
	return rede	

def bkpRede(rede1):
	rede2 = copy.deepcopy(rede1)
	return rede2

#def sigmoide(valor):
#	return ( 1 / ( 1 +math.exp( (-1) * valor) ) )

def sigmoide(gamma):
  if gamma < 0:
    return 1 - 1/(1 + math.exp(gamma))
  else:
    return 1/(1 + math.exp(-gamma))

def derivadaSigmoide(valor):
	return (valor*(1-valor))

def propagacao(rede,entrada):
	
	
	for n in xrange(0,rede.vetNeuroCamada[0]):#cada neuronio da camada de entrada
		saida=0.0
		#print('\n camada ', n)
		for i in xrange(0,rede.entrada):#pra cada peso
			#print('peso do neuro',rede.neuro[0][n].w[i])
			#print('entrada',entrada[i])
			saida= saida + rede.neuro[0][n].w[i]*entrada[i]
			#print('entrada',i)
		saida+=rede.neuro[0][n].bias
		rede.neuro[0][n].saida= sigmoide(saida)
		
	for i in xrange(1,rede.nCamadas):
		for j in xrange(0,rede.vetNeuroCamada[i]):
			saida=0.0
			for k in xrange (0,rede.vetNeuroCamada[i-1]):
				saida+=rede.neuro[i][j].w[k]*rede.neuro[i-1][k].saida
			saida+=rede.neuro[i][j].bias
			rede.neuro[i][j].saida= sigmoide(saida)
				
	return rede

def obtemMelhorClassificador(rede,treinamento,qtdNeuroCam,entradas):
	erro=list(xrange(10))
	for i in xrange(0,10):
		vetResp=[]
		vetEsp=[]
		if(i==0):
			#seleciona o conjunto pra teste e validacao
			treinamento = setTreinamento(treinamento,i)
		
			#fica sobrando uma linha na matriz, entao vrau nela
			x = len(treinamento)
			del treinamento[x-1]
			
			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[i])-1]==0):
					
					rede=propagacao(rede,treinamento[j])

			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[i])-1]==1):	

					rede=propagacao(rede,treinamento[j])

					vetEsp.append(treinamento[j][len(treinamento[i])-2])
					
					vetResp.append(rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
			
			erro[i]=calculaErros(vetEsp,vetResp)

			rede.erroMediaTreino=copy.deepcopy(erro[i])

			redeBKP= bkpRede(rede)

			melhor=i

			del vetResp
			del vetEsp
			
		else:
			vetResp=[]
			vetEsp=[]
			rede=inicializaRede(qtdNeuroCam,entradas)
			#seleciona o conjunto pra teste e validacao
			treinamento = setTreinamento(treinamento,i)
				
			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[i])-1]==0):
					
					rede=propagacao(rede,treinamento[j])
					
			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[i])-1]==1):	
					rede=propagacao(rede,treinamento[j])

					vetEsp.append(treinamento[j][len(treinamento[i])-2])
					
					vetResp.append(rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
			
			erro[i]=calculaErros(vetEsp,vetResp)

			rede.erroMediaTreino=copy.deepcopy(erro[i])
			
			if(rede.erroMediaTreino.medio<redeBKP.erroMediaTreino.medio):
				redeBKP= bkpRede(rede)
				melhor=i

			del vetResp
			del vetEsp
			
	print('o Melhor conjunto foi o ',melhor)		
	media=mediaErros(erro)
	redeBKP.erroMediaTreino=copy.deepcopy(media)
	return redeBKP

def obtemMelhorClassificadorLM(treinamento,entradas):
	erro=list(xrange(10))
	redes =list(xrange(10))
	melhor=-1
	for i in xrange(0,10):
		print '------------------------------------------------'
		print ('Executando o X-Validation para o grupamento ', i)
		print '------------------------------------------------'
		vetResp=[]
		vetEsp=[]
		treino=[]
		validacao=[]
		if(i==0):
			#seleciona o conjunto pra teste e validacao
			treinamento = setTreinamento(treinamento,i)
			#mostraMat(treinamento)
			#fica sobrando uma linha na matriz, entao vrau nela
			x = len(treinamento)
			del treinamento[x-1]
			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[j])-1]==0):
					treino.append(treinamento[j])
			for k in xrange(0,len(treinamento)):
				if(treinamento[k][len(treinamento[k])-1]==1):
					validacao.append(treinamento[k])
			
			rede = pso(treino)
			rede = funcTeste(rede,validacao)
			rede.erroMediaTreino=copy.deepcopy(rede.erroFinal)			
			redeBKP = bkpRede(rede)
			#erro[i]=copy.deepcopy(rede.erroFinal)
			redes[i]=copy.deepcopy(rede)
			melhor=i
			del vetResp
			del vetEsp
			del treino
			del validacao
		else:
			#rede=inicializaRede(qtdNeuroCam,entradas)

			treinamento = setTreinamento(treinamento,i)

			for j in xrange(0,len(treinamento)):
				if(treinamento[j][len(treinamento[i])-1]==0):
					treino.append(treinamento[j])
			for k in xrange(0,len(treinamento)):
				if(treinamento[k][len(treinamento[i])-1]==1):
					validacao.append(treinamento[k])
			rede = pso(treino)
			rede = funcTeste(rede,validacao)
			rede.erroMediaTreino=copy.deepcopy(rede.erroFinal)
			#redeBKP = bkpRede(rede)
			
			#erro[i]=copy.deepcopy(rede.erroFinal)
			redes[i]=copy.deepcopy(rede)
			if(rede.erroMediaTreino.quadratico<redeBKP.erroMediaTreino.quadratico):
				redeBKP= bkpRede(rede)
				melhor=i


			del vetResp
			del vetEsp
			del treino
			del validacao

	print('o Melhor conjunto foi o ',melhor)		
	#media=mediaErros(erro)
	#redeBKP.erroMediaTreino=copy.deepcopy(media)
	return redes

def mErros(rede):
	mediaErros=object.__new__(erro)
	mediaErros.init(0)
	for i in xrange(0,len(rede)):
		mediaErros.medio += (rede[i].erroFinal.medio)/len(rede)
		mediaErros.quadratico += (rede[i].erroFinal.quadratico)/len(rede)
		mediaErros.variancia += (rede[i].erroFinal.variancia)/len(rede)
		mediaErros.dPadrao += (rede[i].erroFinal.dPadrao)/len(rede)

	return mediaErros

def mediaErros(vetErro):
	media = object.__new__(erro)
  	media.init(0)
	medio=0
	variancia=0
	dp=0
	remq=0
	for i in xrange(0,10):
		medio+=vetErro[i].medio
		variancia+=vetErro[i].variancia
		dp+=vetErro[i].dPadrao
		remq+=vetErro[i].quadratico
	media.medio=medio/10
	media.variancia=variancia/10
	media.dPadrao=dp/10
	media.quadratico=remq/10
	
	return media

#validacao da rede treinada
def funcTeste(rede,banco):
	
	vetResp=[]
	vetEsp=[]
	
	#seleciona o conjunto pra teste e validacao
	
	for j in xrange(0,len(banco)):
		
			rede=propagacao(rede,banco[j])
			
			vetEsp.append(banco[j][len(banco[j])-2])
			
			vetResp.append(rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
	
	erro=calculaErros(vetEsp,vetResp)

	rede.erroFinal=copy.deepcopy(erro)
	

	del vetResp
	del vetEsp
	#Retorna o erro medio final do modelo.
	return rede;


def vetEsp(banco):
	for i in xrange(0, (len(banco)) ):
		vetEsperado.append(banco[i][10])

def calculaPesos(rede):
	qtde=0
	for i in xrange(0,rede.nCamadas):
		for j in xrange(0,rede.vetNeuroCamada[i]):	
			qtde+=len(rede.neuro[i][j].w)
	return qtde

#Executa o algoritmo de treinamento Levenberg-Marquardt

def LM(rede,banco):
	#variacao minima do erro
	lambida=0.0001
	v=2
	maxLambida=1000

	#vetores de respostas
	vetEsperado=[]
	vetEncontrado=[]
	#Calcula o numero de pesos da rede neural.
	pesosRede=calculaPesos(rede)

	#gera o vetor de valores esperados
	#vetEsp(banco)
	#print(len(banco))
	#Cria a matriz jacobiana [instancias X pesos]
	#Jacobiana=list(xrange(pesosRede))
	Jacobiana=list(xrange(len(banco)))
	for i in xrange(0,len(banco)):
	#for i in xrange(0,pesosRede):
		Jacobiana[i]=list(xrange(pesosRede))
	#print(len(Jacobiana))
	#print(len(Jacobiana[0]))
	#mostraMat(Jacobiana)
	
	#print(Jacobiana)
	#Cria a matriz de erros [instancias X neuronios na saida] 
	matErro=list(xrange(len(banco))) #no meu caso so tem uma saida

	#Cria as matrizes:
	#- B [pesos X neuronios na saida]
	B = list(xrange(pesosRede))

	# - L e U [pesos X pesos]
	L = list(xrange(pesosRede))
	U = list(xrange(pesosRede))
	#print(pesosRede)
	for i in xrange(0,pesosRede):
		L[i]=list(xrange(pesosRede))
		U[i]=list(xrange(pesosRede))
	#print'len de l'
	#print(len(L))
	#print'len de l[1]'
	#print(len(L[0]))
	# Cria matriz identidade [pesos X pesos]
	Identidade = criaIdentidade(pesosRede)

	# Ate o criterio de parada ser satisfeito [numero de ciclos]
	for i in xrange(0,10):
		#print('Ciclo da LM = ',i)
		#Para todo o conjunto de instancias
		for j in xrange(0,len(banco)):
			#Propaga o sinal pela rede ate a camada de saida.

			rede = propagacao(rede,banco[j])

			#como so tem um neuronio na camada de saida, so faz uma vez
			#joga o valor obtido na camada de saida no vetor de respostas e no de esperados
			vetEncontrado.append(rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
			vetEsperado.append(banco[j][len(banco[j])-2])

			#calcula a diferenca entre a resposta obtida e a esperada e joga na matriz de erros
			matErro[j]= vetEsperado[j]-vetEncontrado[j]

			#Retropropaga o erro
			rede = retro(rede)

			# Calcula a matriz Jacobiana
			count_Peso = 0
			#para cada camada da rede
			for x in xrange(0,rede.nCamadas):
				#para cada neuronio da camada
				for y in xrange(0,rede.vetNeuroCamada[x]):
					# Caso for a primeira camada, o numero de pesos de cada neuronio sera o numero de atributos
					if(x==0):
						for w in xrange(0,rede.entrada):
							Jacobiana[j][count_Peso] = (banco[j][w]*rede.neuro[x][y].w[w]*rede.neuro[x][y].delta)
							#jacobiana[inst][peso]=saidaneuro*peso*delta(backpropagation)
							count_Peso+=1
					else:
						for z in xrange(1,rede.vetNeuroCamada[x-1]):
							# IMPORTANTE: Este calculo nao deve ser implementado agora !!!
							#jacobiana[inst][peso]=saidaneuro*peso*delta(backpropagation)
							Jacobiana[j][count_Peso] = (rede.neuro[x-1][z].saida*rede.neuro[x][y].w[z]*rede.neuro[x][y].delta)
							
							count_Peso+=1
		#mostraMat(Jacobiana)
	
		#Fim da criacao da matriz Jacobiana.	
		rede = funcTeste(rede,banco)
		#print('erro fora',rede.erroFinal.quadratico)
		#mostraMat(Jacobiana)
		#print(Jacobiana)
		#Calcula matriz transposta da Jacobiana
		JacobianaTransposta = Transposta(Jacobiana)
		
		#Calcula matriz Jacobiana * 2
		JacobianaTranspostax2 = multiplicaConstante(JacobianaTransposta, 2)
		
		#Calcula matriz Gradiente do erro (Gradiente = JacobianaTransposta X matriz de erros na saida)
		Gradiente = multMat(1,JacobianaTransposta, matErro)
		#Gradiente = tadMatriz_Multiplica(JacobianaTranspostax2, matrizDeErros);
		
		#Calcula matriz Hessiana (H = JacobianaTransposta x Jacobiana)
		Hessiana = multMat(len(Jacobiana[0]),JacobianaTransposta, Jacobiana)
		#Hessiana = tadMatriz_Multiplica(JacobianaTranspostax2, Jacobiana);
		
		#Copia Gradiente para matriz B que serah usada na resolucao do sistema linear.

		for z in xrange(0,pesosRede):
	   		B[z]= Gradiente[z]
			
		fimCiclo=0
		while((fimCiclo==0) and (lambida<maxLambida)):
			#Calcula matriz Identidade x Lambda
			identidadexLambda = multiplicaConstante(Identidade, lambida)

			#Calcula matriz Hessiana, ja acrescentando o Lambda na diagonal da matriz.
			ajusteHessiana = somaMat(Hessiana, identidadexLambda)
			
			#Faz a decomposicao LU da matriz Hessiana.
			DecomposicaoLU(ajusteHessiana, L, U)
			
			#Calcula o determinante da matriz U.
   			detHessiana = detU(pesosRede, U)
 			#detHessiana =1
			#Verifica se matriz Hessiana eh singular
   			if (detHessiana > 0.0): 
				#Resolve o sistema (Hessiana + Lambda x Identidade) * Solucao = B
				#A matriz solucao eh composta pelos novos pesos.
				solucao = resolveDecomposicaoLU(len(B),len(B[0]),L, U, B)
				
				
				#Faz backup dos pesos pois, caso o resultado seja pior que o anterior
				redeBKP = bkpRede(rede)
				#os pesos gerados sao descartados.
				
				#Atualiza os pesos com a solucao gerada.
				iPeso=0
				for k in xrange(0,rede.nCamadas):
					for n in xrange(0,rede.vetNeuroCamada[k]):
						if (k==0):
							for m in xrange(0,rede.entrada):
								rede.neuro[k][n].w[m]=rede.neuro[k][n].w[m]-solucao[iPeso][0]
								iPeso+=1
						else:
							for m in xrange(0,rede.vetNeuroCamada[k-1]):
								rede.neuro[k][n].w[m]=rede.neuro[k][n].w[m]-solucao[iPeso][0]
								iPeso+=1

				#Refaz teste sobre o conjunto
				rede = funcTeste(rede,banco)
				
				#print('erro dentro',rede.erroFinal.quadratico)
				
				#Verifica se pesos encontrados sao melhores que anteriores
				if(redeBKP.erroFinal.quadratico < rede.erroFinal.quadratico):
					#Desfaz atualizacao dos pesos.
					rede=bkpRede(redeBKP)
					#Incrementa Lambda e refaz calculo de pesos
					lambida = lambida * v
					fimCiclo = 0
				
				else:
					#Caso os pesos sao melhores, decrementa lambda (amortece o aprendizado) e inicia proximo ciclo.
					lambida = lambida / v
					fimCiclo = 1
				
				
				#Libera memoria usada para o vetor solucao
				#del identidadexLambda
	   		
	   		#se hessiana for singular
	   		else: 
	   			fimCiclo = 1
	   		

	   		#Libera memoria usada para matrizes alocadas no ciclo
			#del identidadexLambda
			#del ajusteHessiana
		#del JacobianaTransposta
		#del JacobianaTranspostax2
		#del Gradiente
		#del Hessiana

	#Libera matriz alocadas no inicio do processamento.
	#del matErro
	#del B
	#del L
	#del U
	#del Jacobiana
	#del Identidade
	
	#print 'foi pro proximo \n'
	return rede
		

def retro(rede):
	c = rede.nCamadas-1
	for i in xrange(0,rede.vetNeuroCamada[c]):
		rede.neuro[c][i].delta = sigmoide(rede.neuro[c][i].saida)

	for c in xrange(rede.nCamadas-2,-1,-1):
		for n in xrange(0,rede.vetNeuroCamada[c]):
			erro=0.0
			for e in xrange(0,rede.vetNeuroCamada[c+1]):
				erro+= (rede.neuro[c+1][e].w[n]*rede.neuro[c+1][e].delta)
			rede.neuro[c][n].erro=erro
			rede.neuro[c][n].delta=erro * sigmoide(rede.neuro[c][n].saida)

	return rede


def ajustaPesos(rede,banco):
	ajuste=0
	#Ajusta os pesos dos neuronios da camada de entrada.
	for n in xrange(0,rede.vetNeuroCamada[0]):
		for e in xrange(0,rede.entrada):
			ajuste=(rede.taxaAprendizado * rede.neuro[0][n].delta * banco[e])
			rede.neuro[0][n].w[e] += (ajuste+ (rede.momentum * rede.neuro[0][n].dw[e]) )
			rede.neuro[0][n].dw[e] = ajuste

		ajuste = rede.taxaAprendizado * rede.neuro[0][n].delta
		rede.neuro[0][n].bias += ajuste + (rede.momentum * rede.neuro[0][n].dbias)
		rede.neuro[0][n].dbias = ajuste 

	# Ajusta os pesos dos neuronios das demais camadas.
	for c in xrange(1,rede.nCamadas):
		for n in xrange(0,rede.vetNeuroCamada[c]):
			for e in xrange(0,rede.vetNeuroCamada[c-1]):
				ajuste = (rede.taxaAprendizado * rede.neuro[c][n].delta * rede.neuro[c-1][e].saida)
				rede.neuro[c][n].w[e] += (ajuste + (rede.momentum * rede.neuro[c][n].dw[e]))
				
				rede.neuro[c][n].dw[e] = ajuste
			
			ajuste = (rede.taxaAprendizado * rede.neuro[c][n].delta)
			rede.neuro[c][n].bias += (ajuste + (rede.momentum * rede.neuro[c][n].dbias))
			rede.neuro[c][n].dbias = ajuste

	return rede

'''
def algAprendizado(rede,banco):
	count=0



	
	do {
		c = rede.nCamadas-1
		
		# Submete a rede ao aprendizado.
		erro_Medio = 0.0
		for i in xrange(0,len(banco)):
		for (int i=0; i<setLocal.num_Instancias; i++) {
			# Propaga o sinal pela rede.
			rede = propagacao(rede,banco[i])
			
			#Calcula o erro para cada neuronio de saida.
			for n in xrange(0,rede.vetNeuroCamada[c]):
			for(n=0; n<varIA_MLP.RNA.qtd_NeurCamadas[c]; n++) {
				#Verificar o valor esperado e o obtido.
				
				
				# Calcula o erro do neuronio.
				varIA_MLP.RNA.rede[c][n].erro = bit - varIA_MLP.RNA.rede[c][n].saida
				erro_Medio += varIA_MLP.RNA.rede[c][n].erro
			}
			
			#Retropropaga (backpropagation) o erro calculado.
			fncIA_MLP_BackPropagation_RetropropagaErro();
			
			#Ajusta os pesos dos neuronios.
			fncIA_MLP_BackPropagation_AjustaPesos(setLocal.insts[i].atributos, setLocal.num_Atributos)
		}
		# Atualiza condicoes de parada.
		erro_Medio = (float) erro_Medio / (varIA_MLP.RNA.qtd_NeurCamadas[c] * setLocal.num_Instancias)
		count+=1
	} while ((erro_Medio < varIA_MLP.RNA.maxErro) && (count < varIA_MLP.RNA.maxCiclos)); #Condicoes de parada.
	
	return true;
}'''

class Particula(object):
	def init(self,camadas):
		#configuracao atual de neuronios
		self.x=list(xrange(camadas))
		#melhor erro da particula
		self.pBestFun=0.0
		#velocidade com a qual a particula vai 'andar'
		self.speed=list(xrange(camadas))
		#erro atual da particula
		self.func=0.0
		#guarda a melhor configuracao de neuroninios ate o momento
		self.pBest=list(xrange(camadas))
		
				
class Enxame(object):
	def init(self,numParticulas,minNeuro,maxNeuro):
		#posicao do vetor de particulas onde se encontra a melhor
		self.gBest=0
		#vetor de particulas
		self.vetParticulas=list(xrange(numParticulas))
		#melhor rede do vetor de particulas
		self.melhorRede =0
		#quantidade minima de neuronios por camada
		self.minNeuro=minNeuro
		#quantidade maxima de neuronios por camada
		self.maxNeuro=maxNeuro

def pso(treino):
# ===============
# Passo 1: Iniciar as variaveis do enxame de particulas. Onde:
	enxame=object.__new__(Enxame)

	minneuro = 1
	maxneuro = 8
	numparticulas = 5
	parametros=list(xrange(4))

	parametros[0]=9
	parametros[3]=1

	enxame.init(numparticulas,minneuro,maxneuro)
	#enxame.init(10,2,15)
	#dentro de cada posicao do vetor, sera criado uma particula
	for i in xrange(0,len(enxame.vetParticulas)):
		enxame.vetParticulas[i]=object.__new__(Particula)
		enxame.vetParticulas[i].init(2)
		
# - Inicializar os valores das particulas (i = particula, j = elemento da particula):
# - a velocidade da particula:- V[i][j] = ((j_max - j_min) * <sorteio de um valor aleatorio>) - X[i][j],para toda particula;
	for i in xrange(0,len(enxame.vetParticulas)):
		for j in xrange(0,len(enxame.vetParticulas[i].x)):
			enxame.vetParticulas[i].x[j]=random.randrange(minneuro, maxneuro+1)
			enxame.vetParticulas[i].speed[j]=((maxneuro-minneuro) * random.random() ) - enxame.vetParticulas[i].x[j]

# - Definir outras variavies:
	for i in xrange(0,len(enxame.vetParticulas[i].pBest)):
		enxame.vetParticulas[i].pBest[i]=0

	enxame.vetParticulas[i].pBestFun=0
	enxame.gBest=0
	enxame.melhorRede=inicializaRede(parametros,9)
	enxame.melhorRede.erroFinal=object.__new__(erro)
	enxame.melhorRede.erroFinal.quadratico=100
#- Gbestfun (inicialmente 0) representa o valor da funcao objetivo da melhor particula; ( vou guardar a melhor rede que ja tem o erro)

#- N eh o tamanho do enxame (numero de particulas);
 	w = 0.1
 	#w = 1/(2*math.log(2,10)) #ponderacao da inercia;
	c_1 = 0.5 + math.log(2,10) #representa o parametro cognitivo;
	c_2 = c_1 #representa o parametro social.
# ===============
# Passo 2: Calcular o valor da funcao-objetivo f(X) para todas as particulas.

	print '----------------------------------------------'
	print '    Inicializando as particulas do PSO  		 '
	print '----------------------------------------------'

	for i in xrange(0,len(enxame.vetParticulas)):
		parametros[1]=enxame.vetParticulas[i].x[0]
		parametros[2]=enxame.vetParticulas[i].x[1]

		rede = inicializaRede(parametros,9)
		#print '\n'
		print '------------------------------'
		#print 'config rede \n'
		print('config rede = ',rede.vetNeuroCamada)
		print '------------------------------'
		#print '\n'
		

		rede = LM(rede,treino)
		#quantidade de camadas(2)
		for j in xrange(0,len(enxame.vetParticulas[i].pBest)):
			#- O vetor Pbest[i] recebe a posicao atual de cada particula;
			enxame.vetParticulas[i].pBest[j]  =  enxame.vetParticulas[i].x[j]
			#- O vetor Pbestfun[i] recebe o valor da funcao-objetivo da particula;
		enxame.vetParticulas[i].pBestFun  =  rede.erroFinal.quadratico
		enxame.vetParticulas[i].func  =  rede.erroFinal.quadratico
			#- Gbest recebe a posicao da melhor particula do enxame;
			#- Gbestfun recebe a funcao-objetivo da melhor particula do enxame.
		if(enxame.melhorRede.erroFinal.quadratico > rede.erroFinal.quadratico ):
			enxame.gBest=i
			enxame.melhorRede = bkpRede(rede)
# ===============
# Passo 3: Atualizar as posicoes e velocidades das particulas de acordo com asequacoes a seguir:
# ===============
# Passo 4: Calcular o valor da funcao-objetivo f(X) para todas as particulas considerando a quantidade de neuronios na camada escondida.
# ===============
# Passo 5: Para cada particula, comparar o valor da funcao-objetivo atual com o
#valor de Pbest[i]. Caso o atual seja melhor, Pbest[i] recebe a posicao atual e
#Pbestfun[i] recebe o valor da funcao-objetivo atual.
# ===============
# Passo 6: Encontrar o melhor valor objetivo entre as particulas atuais e comparar com o Gbest. Caso haja melhora, Gbest recebe a posicao e Gbestfun recebe a funcao-objetivo da melhor particula.
# ===============
# Passo 7: Repetir o processo a partir do Passo 3 ateh que uma condicao de parada seja encontrada.
# ===============
# Exemplo de implementacao para os Passos 3 ao 7:
# Enquanto o criterio de parada nao for satisfeito, faca:
	ciclo=0

	print '------------------------------'
	print 'Comecou realmente o PSO       '
	print '------------------------------'

	while(ciclo<10):
		print '----------------------------'
		print('Ciclo ', ciclo)
		print '----------------------------'
		# Para cada particula do enxame, faca:
		#Passo 3: Atualizar as posicoes e velocidades das particulas de acordo com asequacoes a seguir:
		for i in xrange(0,len(enxame.vetParticulas)):
		# Para cada dimensao, faca:
			print('Particula ', i)
			for d in xrange(0,len(enxame.vetParticulas[i].pBest)):
				# Escolha valores aleatorios entre 0 e 1.
				rp = random.random()
				rg = random.random()
				# Atualize a velocidade da particula.
				enxame.vetParticulas[i].speed[d] = (w * enxame.vetParticulas[i].speed[d]) + (c_1*rp*(enxame.vetParticulas[i].pBest[d] - enxame.vetParticulas[i].x[d])) + (c_2*rg*(enxame.vetParticulas[enxame.gBest].pBest[d] - enxame.vetParticulas[i].x[d]))
				#atualiza a posicao da particula	
			
				enxame.vetParticulas[i].x[d] =enxame.vetParticulas[i].x[d] + enxame.vetParticulas[i].speed[d]
				#print('Velocidade atual = ',enxame.vetParticulas[i].speed[d])
				#print('Posicao da particula atual = ',enxame.vetParticulas[i].x[d])
	# ===============
		#Passo 4: Calcular o valor da funcao-objetivo f(X) para todas as particulas considerando a quantidade de neuronios na camada escondida.		
		#for i in xrange(0,len(enxame.vetParticulas)):
			if(enxame.vetParticulas[i].x[0]>maxneuro):
				enxame.vetParticulas[i].x[0]=maxneuro

			if(enxame.vetParticulas[i].x[1]>maxneuro):
				enxame.vetParticulas[i].x[1]=maxneuro

			if(enxame.vetParticulas[i].x[0]<minneuro):
				enxame.vetParticulas[i].x[0]=minneuro

			if(enxame.vetParticulas[i].x[1]<minneuro):
				enxame.vetParticulas[i].x[1]=minneuro


			parametros[1]=int(enxame.vetParticulas[i].x[0])
			parametros[2]=int(enxame.vetParticulas[i].x[1])
			#print '\n camada 1 \n'
			#print(enxame.vetParticulas[i].x[0])
			#print '\n camada 2 \n'
			#print(enxame.vetParticulas[i].x[1])
			print (parametros)
			rede = rede = inicializaRede(parametros,9)
			rede = LM(rede,treino)
			enxame.vetParticulas[i].func=rede.erroFinal.quadratico
			if (enxame.vetParticulas[i].func < enxame.vetParticulas[i].pBestFun):
				#for j in xrange(0,len(enxame.vetParticulas[i].pBest)):
				#- O vetor Pbest[i] recebe a posicao atual de cada particula;
				enxame.vetParticulas[i].pBest  =  enxame.vetParticulas[i].x
				#- Pbestfun[i] recebe o valor da funcao-objetivo da particula;
				enxame.vetParticulas[i].pBestFun  =  rede.erroFinal.quadratico
				#- Gbest recebe a posicao da melhor particula do enxame;
				#- Gbestfun recebe a funcao-objetivo da melhor particula do enxame.
			if(enxame.melhorRede.erroFinal.quadratico > rede.erroFinal.quadratico ):
				enxame.gBest=i
				enxame.melhorRede = bkpRede(rede)
			# Atualiza o criterio de parada.
		
		ciclo+=1

	return enxame.melhorRede
