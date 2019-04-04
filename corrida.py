import pandas as pd
import numpy as np
import datetime
from decimal import *

#Leitura do arquivo
df3 = pd.read_csv('corrida_kart.txt', sep='\s+')
arquivo_tratado = df3
#Tratamento de colunas
arquivo_tratado["Código Piloto"] = df3.Piloto.str[:3]
arquivo_tratado["Nome Piloto"] = df3.Piloto.str[4:]
#Removendo Coluna sem uso
arquivo_tratado.drop(["Piloto"], axis=1)
#Renomeando colunas
arquivo_tratado.rename(columns={"TempoVolta" : "Tempo Volta", "VelocidadeMediaDaVolta": "Velocidade Media Da Volta"}, inplace=True)
# Ordenando arquivo para somar tempo de volta
arquivo_tratado.sort_values(['Código Piloto','Volta'], inplace=True)
# Pegar o maior número de voltas que o corredor deu
voltas = arquivo_tratado.groupby("Código Piloto")["Volta"].max()

#Faz o calculo do tempo total de corrida por corredor
def somaVoltas(linhas):
  linhas["Tempo Total de Prova"] = ""
  ma, sa, msa = 0,0,0
  for indice, linha in linhas.iterrows():
    tempo = linha["Tempo Volta"].replace('.', ':')
    if linha["Volta"] == voltas[linha["Código Piloto"]]:
      m, s, ms = tempo.split(':')
      ma = ma + int(m)
      sa = sa + int(s)
      msa = msa + int(ms)
      if msa > 999:
        sa = sa + 1
        msa = 999
      elif msa > 1999:
        sa = sa + 2
        msa = 999
      if sa > 60:
        ma = ma + 1
        sa = 60
      linhas.loc[indice, "Tempo Total de Prova"] = str(ma) + ":" + str(sa) + "." + str(msa)
      ma, sa, msa = 0,0,0
    else:
      m, s, ms = tempo.split(':')
      ma = ma + int(m)
      sa = sa + int(s)
      msa = msa + int(ms)
  return linhas

#Faz o calculo do tempo medio das voltas
def velocidadeMedia(linhas):
  linhas["Velocidade Media Corrida"] = ""
  velocidade = Decimal(0)
  for indice, linha in linhas.iterrows():
    if linha["Volta"] == voltas[linha["Código Piloto"]]:
      velocidade = velocidade + Decimal(str(linha["Velocidade Media Da Volta"]).replace(',','.'))
      linhas.loc[indice, "Velocidade Media Corrida"] = velocidade / int(voltas[linha["Código Piloto"]])
      velocidade = Decimal(0)
    else:
      velocidade = velocidade + Decimal(str(linha["Velocidade Media Da Volta"]).replace(',','.'))
  return linhas

#Retorna o resultado da corrida com base nas funcoes
def resultadoCorrida():
    retorno = somaVoltas(arquivo_tratado)
    retorno = velocidadeMedia(retorno)
    retorno = retorno[retorno["Tempo Total de Prova"] != ""]
    retorno.rename(columns={"Volta" : "Qtde Voltas Completadas"}, inplace=True)
    retorno = retorno.drop(["Hora", "Piloto", "Tempo Volta"], axis=1)
    retorno.sort_values(['Tempo Total de Prova', 'Qtde Voltas Completadas'], inplace=True)

    posicao = 1
    retorno["Posição"] = ""
    
    for indice, linha in retorno.iterrows():
        retorno.loc[indice, "Posição"] = posicao
        posicao += 1

    retorno.set_index('Código Piloto', inplace=True)
    return retorno