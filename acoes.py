import os
import math
import time
import sys
import copy
import random
import timeit
from preproc import *
from mlp import *
from funcs import *
from opMat import *
#from psopy import *
def main():
        escolha =1
        carregaNovo=0
        exibe=1
        tempoPreproc=0
        mat=[]
        gera=[]
        normalizado=[]
        treinamento=[]
        teste=[]
        erros=[]
        rede=[]
        while (escolha!=0):
          print('\n------------O que deseja fazer?------------\n')
          escolha = int(input('  1 - Selecionar Arquivo \n  2 - Pre-Processamento \n  3 - Imprimir o BD  \n  4 - Cross-Validation e K-fold  \n  5 - Testar a rede  \n  9 - Developer Area  \n  0 - Sair\n'))
          if (escolha==1):
            i=timeit.default_timer()
            #nome_arq = raw_input('Entre com o nome do arquivo de dados\n=>')
            #arq = open(nome_arq+'.txt', 'r')
            arq = open('13-17-2.txt', 'r')
            mat = le_matriz(arq.readlines())
            #mostraMat(mat)
            f=timeit.default_timer()
            tempoPreproc=(f-i)
            print('Tempo de Execucao =%f' %(tempoPreproc))
          
          #preprocessamento
          elif (escolha==2):
            i=timeit.default_timer()
            gera=geraMedias(mat)
            #mostraMat(gera)
            normalizado=normaliza(gera)

            f=timeit.default_timer()
            tempoPreproc=(f-i)
            print('Tempo de Execucao =%f' %(tempoPreproc))
          
          #impressao do banco  
          elif (escolha==3):
            i=timeit.default_timer()

            mostraMat(normalizado)
            #print(normalizado[len(normalizado)-1])

            f=timeit.default_timer()
            tempoPreproc=(f-i)
            print('\n')
            print('Tempo de Execucao =%f' %(tempoPreproc))

          # X-Validation e k-fold , impressao da media dos erros
          elif (escolha==4):
			i=timeit.default_timer()
			'''
			random.shuffle(normalizado) 

			#seleciona o conjunto de teste e o coloca na matriz teste
			teste = selecionaTeste(normalizado)           

			rede = inicializaRede((4,3,4,5,6,1),9)

			rede= obtemMelhorClassificador(rede,normalizado,(4,3,4,5,6,1),9)'''

			teste = selecionaTeste(normalizado)           
			#rede = inicializaRede((4,3,4,5,6,1),9)
			#rede = inicializaRede((9,4,1),9)
			#rede2=LM(rede2,normalizado,teste)
			#rede = obtemMelhorClassificadorLM(rede,normalizado,(4,3,4,5,6,1),9)
			#rede = obtemMelhorClassificadorLM(rede,normalizado,(9,4,1),9)
			redes = obtemMelhorClassificadorLM(normalizado,9)
			rede = bkpRede(redes[0])
			print('tamanho do vetor redes = ', len(redes))
			for i in range(0,len(redes)):
				print(' iteracoes = ', i )
				if (redes[i].erroFinal.quadratico < rede.erroFinal.quadratico):
					rede = bkpRede(redes[i])
					melhor = i
				print('Rede numero ', i+1)
				print('Configuracao da rede = ',redes[i].vetNeuroCamada)
				print('Erro medio quadratico',redes[i].erroMediaTreino.quadratico)
				print('\n')

			  
			#mostraMat(teste)
			#rede = retro(rede)
			print('A melhor rede foi a ', melhor)
			medErros = mErros(redes)
			print('qtde neuro camada = ',rede.vetNeuroCamada)
			#print('Saida', rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
			print('\n')
			print('Media dos erros das 10 redes treinadas')
			#print('\n')
			print('Erro medio',medErros.medio)
			print('Erro variancia',medErros.variancia)
			print('Erro medio quadratico',medErros.quadratico)
			print('Erro desvio padrao',medErros.dPadrao)
			print('\n')	
			#print('erro neuronio',rede.neuro[0][0].erro)
			#print('delta neuronio',rede.neuro[0][0].delta)
			
			f=timeit.default_timer()
			tempoPreproc=(f-i)

			print('\n')
			print('Tempo de Execucao =%f' %(tempoPreproc))


          #teste com o respectivo conjunto e impressao dos erros reais
          elif (escolha==5):
            i=timeit.default_timer()
            #teste = selecionaTeste(normalizado)    
            rede = funcTeste(rede,teste)

            print('Saida', rede.neuro[rede.nCamadas-1][rede.vetNeuroCamada[rede.nCamadas-1]-1].saida)
            print('Erro medio das rede apos o teste')
            #print('\n')
            print('Erro medio',rede.erroFinal.medio)
            print('Erro variancia',rede.erroFinal.variancia)
            print('Erro medio quadratico',rede.erroFinal.quadratico)
            print('Erro desvio padrao',rede.erroFinal.dPadrao)
            print('\n') 

            f=timeit.default_timer()
            tempoPreproc=(f-i)

            print('\n')
            print('Tempo de Execucao =%f' %(tempoPreproc))
          #elif (escolha==6):
          #elif (escolha==7):
      	     #elif (escolha==8):
          elif(escolha==9):
			i=timeit.default_timer()

			rede = inicializaRede((9,4,3,1),9)
			#rede.erroFinal = object.__new__(erro)
			#rede.erroFinal.init(0)
			#teste = selecionaTeste(normalizado)           
			rede = LM(rede,normalizado)
			for i in range(0,10):
				salvar = guardaRede(rede,i+1)
				if (salvar== 0):
					print('Configuracoes da rede Salvos com sucesso \n')
				else:
					print('Falha ao salvar as configuracoes da rede\n')	    	  
			#print('Erro medio',rede.erroFinal.medio)
			#print('Erro variancia',rede.erroFinal.variancia)
			#print('Erro medio quadratico',rede.erroFinal.quadratico)
			#print('Erro desvio padrao',rede.erroFinal.dPadrao)
			#print('\n')
			#p= pso(normalizado,teste)  
			#print(p.melhorRede.vetNeuroCamada)
			#print(p.melhorRede.erroFinal.quadratico)
			#coe = guardaRede(p.melhorRede)
			#if (coe== 0):
			# 	print('Deu bom \n')
			# else:
			# 	print('Deu ruim\n')
			f=timeit.default_timer()
			tempoPreproc=(f-i)
			print('Tempo de Execucao =%f' %(tempoPreproc))


            
            
main()
