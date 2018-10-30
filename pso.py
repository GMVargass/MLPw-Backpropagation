#ncamadas = 2
import math
import random 
from mlp import *
#nparticulas = x
#nNeuroniios = 1~15
class Particula(object):
	def init(self,camadas):
		#configuracao atual de neuronios
		self.x=list(range(camadas))
		#melhor erro da particula
		self.pBestFun=0.0
		#velocidade com a qual a particula vai "andar"
		self.speed=list(range(camadas))
		#erro atual da particula
		self.func=0.0
		#guarda a melhor configuracao de neuroninios ate o momento
		self.pBest=list(range(camadas))
		
				
class Enxame(object):
	def init(self,numParticulas,minNeuro,maxNeuro):
		#posicao do vetor de particulas onde se encontra a melhor
		self.gBest=0
		#vetor de particulas
		self.vetParticulas=list(range(numParticulas))
		#melhor rede do vetor de particulas
		self.melhorRede
		#quantidade minima de neuronios por camada
		self.minNeuro=minNeuro
		#quantidade maxima de neuronios por camada
		self.maxNeuro=maxNeuro

def pso(treino,teste):
# ===============
# Passo 1: Iniciar as variaveis do enxame de particulas. Onde:
	enxame=object.__new__(Enxame)

	minneuro = 2
	maxneuro = 15
	numparticulas = 10
	parametros=list(range(4))

	parametros[0]=9
	parametros[3]=1

	enxame.init(numparticulas,minneuro,maxneuro)
	#enxame.init(10,2,15)
	#dentro de cada posicao do vetor, sera criado uma particula
	for i in range(0,len(enxame.vetParticulas)):
		enxame.vetParticulas[i]=object.__new__(Particula)
		enxame.vetParticulas[i].Particula.init(2)
		
# - Inicializar os valores das particulas (i = particula, j = elemento da particula):
# - a velocidade da particula:- V[i][j] = ((j_max - j_min) * <sorteio de um valor aleatorio>) - X[i][j],para toda particula;
	for i in range(0,len(enxame.vetParticulas)):
		for j in range(0,len(enxame.vetParticulas[i])):
			enxame.vetParticulas[i].x[j]=random.randrange(minneuro, maxneuro)
			enxame.vetParticulas[i].speed[j]=((maxneuro-minneuro) * random.ramdom() ) - enxame.vetParticulas[i].x[j]

# - Definir outras variavies:
	for i in range(0,len(enxame.vetParticulas[i].pBest)):
		enxame.vetParticulas[i].pBest[i]=0

	enxame.vetParticulas[i].pBestFun=0
	enxame.gBest=0
	enxame.melhorRede=inicializaRede(parametros,9)
	enxame.melhorRede.erroFinal.quadratico=100
#- Gbestfun (inicialmente 0) representa o valor da funcao objetivo da melhor particula; ( vou guardar a melhor rede que ja tem o erro)

#- N eh o tamanho do enxame (numero de particulas);
 	w = 1/(2*math.log(2,10)) #ponderacao da inehrcia;
	c_1 = 0.5 + math.log(2,10) #representa o parametro cognitivo;
	c_2 = c_1 #representa o parametro social.
# ===============
# Passo 2: Calcular o valor da funcao-objetivo f(X) para todas as particulas.
	for i in range(0,len(enxame.vetParticulas)):
		parametros[1]=enxame.vetParticulas[i].x[0]
		parametros[2]=enxame.vetParticulas[i].x[1]

		rede = rede = inicializaRede(parametros,9)
		rede = LM(rede,treino,teste)
		for j in range(0,len(enxame.vetParticulas[i].pBest)):
			#- O vetor Pbest[i] recebe a posicao atual de cada particula;
			enxame.vetParticulas[i].pBest[j]  =  enxame.vetParticulas[i].x[j]
			#- O vetor Pbestfun[i] recebe o valor da funcao-objetivo da particula;
		enxame.vetParticulas[i].pBestFun  =  rede.erroFinal.quadratico
			#- Gbest recebe a posicao da melhor particula do enxame;
			#- Gbestfun recebe a funcao-objetivo da melhor particula do enxame.
		if(enxame.melhorRede.erroFinal.quadratico > rede.erroFinal.quadratico ):
			gBest=i
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
	while(ciclo<100):
		# Para cada particula do enxame, faca:
		#Passo 3: Atualizar as posicoes e velocidades das particulas de acordo com asequacoes a seguir:
		for i in range(0,len(enxame.vetParticulas)):
		# Para cada dimensao, faca:
			for d in range(0,len(enxame.vetParticulas[i].pBest)):
				# Escolha valores aleatorios entre 0 e 1.
				rp = random.random()
				rg = random.random()
				# Atualize a velocidade da particula.
				enxame.vetParticulas[i].speed[d] = (w * enxame.vetParticulas[i].speed[d]) + (c_1*random.random()*(enxame.vetParticulas[i].pBest[d] - enxame.vetParticulas[i].x[d])) + (c_2*random.random()*(enxame.vetParticulas[gBest].pBest[d] - enxame.vetParticulas[i].x[d]))
					
				enxame.vetParticulas[i].x[d] =enxame.vetParticulas[i].x[d] + enxame.vetParticulas[i].speed[d]
	# ===============
		#Passo 4: Calcular o valor da funcao-objetivo f(X) para todas as particulas considerando a quantidade de neuronios na camada escondida.		
		for i in range(0,len(enxame.vetParticulas)):
			parametros[1]=enxame.vetParticulas[i].x[0]
			parametros[2]=enxame.vetParticulas[i].x[1]

			rede = rede = inicializaRede(parametros,9)
			rede = LM(rede,treino,teste)
			for j in range(0,len(enxame.vetParticulas[i].pBest)):
				#- O vetor Pbest[i] recebe a posicao atual de cada particula;
				enxame.vetParticulas[i].pBest[j]  =  enxame.vetParticulas[i].x[j]
				#- O vetor Pbestfun[i] recebe o valor da funcao-objetivo da particula;
			enxame.vetParticulas[i].pBestFun  =  rede.erroFinal.quadratico
				#- Gbest recebe a posicao da melhor particula do enxame;
				#- Gbestfun recebe a funcao-objetivo da melhor particula do enxame.
			if(enxame.melhorRede.erroFinal.quadratico > rede.erroFinal.quadratico ):
				gBest=i
				enxame.melhorRede = bkpRede(rede)
			# Atualiza o criterio de parada.


	return enxame
