
import pandas as pd
import re 
from datetime import datetime


## Etapas da construção

## Abrir o arquivo de presença


# Lê o arquivo de presença
file = 'presenca.xlsx'

# Celula inicial (b15)
#init_cell = 'b15'

# Lê a planilha de presença
dados = pd.read_excel(file, sheet_name='Folha1', header=None, skiprows=lambda x: x < 14)
dados_2 = pd.read_excel(file, sheet_name='Folha2', header=None, skiprows=lambda x: x < 13)

# Informações da turma
dados_turma_1 = pd.read_excel(file, sheet_name='Folha1', date_format='%d/%m/%Y %H:%M:%S',parse_dates= True)
dados_turma_2 = pd.read_excel(file, sheet_name='Folha2', date_format='%d/%m/%Y %H:%M:%S',parse_dates= True)


# Coletando informações da turma (sem recursividade)
linha = 12
coluna = 1
df_turma_1 = dados_turma_1.iloc[linha, coluna]
# Na Planilha 2 a linha é 13
df_turma_2 = dados_turma_2.iloc[linha - 1 , coluna]

# print(df_turma_1)
#print(df_turma_2)


# Limpando as colunas que não serão utilizadas
df = dados.drop(dados.columns[[0, 2, 4, 5, 6, 8, 9, 11, 13, 14, 16, 17 ]], axis=1)
df_2 = dados_2.drop(dados_2.columns[[0, 2, 4, 5, 6, 8, 9, 11, 13, 14, 16, 17 ]], axis=1)


# Expressão regular para coletar o código da turma
padrao = r'^.{24}'

turma_1 = re.findall(padrao, df_turma_1)
turma_2 = re.findall(padrao, df_turma_2)

# print(turma_1)
# print(turma_2)

# Coletando a data da aula (sem recursividade)


# data_plan = datetime.strptime(df_data, "%Y/%m/%d %H:%M:%S")
# data_final = datetime.strftime(data_plan, "%d/%m/%Y %H:%M:%S")
# df_data =  datetime.strftime("%d/%d/%Y, %H:%M:%S")

# data_str = str(df_data)
# print(df_data)

# Removendo a primeira linha (cabeçalho)
df = df.drop(df.index[0])
df_2 = df_2.drop(df_2.index[0])


# Renomeando as colunas
df.columns = ['Matricula', 'Nome', 'Unidade do Parceiro', 'Entrada', 'Saída', 'Assinatura', 'Atraso', 'Nota']
df_2.columns = ['Matricula', 'Nome', 'Unidade do Parceiro', 'Entrada', 'Saída', 'Assinatura', 'Atraso', 'Nota']

df.insert(0, 'Turma', turma_1[0])
df_2.insert(0, 'Turma', turma_2[0])

print(df)
print(df_2)

#tipo = type(df)
#mensagem = "O tipo de dados é df: {}".format(tipo)
#print(mensagem)


# tipo_2 = type(df_2)
# mensagem = "O tipo de dados é df_2: {}".format(tipo_2)
# print(mensagem)


#df.to_excel('df.xlsx', index=False)

# df_2 = df_2.insert(0, 'Turma', turma_2[0])
# df_2.to_excel('df_2.xlsx', index=False)


# df_2 = df_2.insert(0, 'Turma', turma_2[0])

# concatenando os dois dataframes
alunos = pd.concat([df, df_2],ignore_index=True)

# exportando para csv (para testes)
alunos.to_excel('alunos.xlsx', index=False)

# Todo: 1 - Verificar se a planilha com a presença dos alunos está no formatada
#       2 - Futuramente colocar um laço de repetição para verificar até a ultima planilha da pasta
#       3 - Criar um filtro para verificar se a coluna é NaN e remover a coluna de uma forma recursiva
#       4 - Fazer a leitura da data da aula
#       5 - Diminuir as gambiarras
