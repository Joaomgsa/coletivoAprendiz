
import pandas as pd

## Etapas da construção

## Abrir o arquivo de presença


# Lê o arquivo de presença
file = 'presenca.xlsx'

# Celula inicial (b15)
init_cell = 'b15'

# Lê a planilha de presença
dados = pd.read_excel(file, sheet_name='Folha1', header=None, skiprows=lambda x: x < 14)
dados_2 = pd.read_excel(file, sheet_name='Folha2', header=None, skiprows=lambda x: x < 14)

## planilha1 = pd.read_excel(file, sheet_name='Folha1')

# Limpando as colunas que não serão utilizadas
df = dados.drop(dados.columns[[0, 2, 4, 5, 6, 8, 9, 11, 13, 14, 16, 17 ]], axis=1)
df_2 = dados_2.drop(dados_2.columns[[0, 2, 4, 5, 6, 8, 9, 11, 13, 14, 16, 17 ]], axis=1)

# Removendo a primeira linha (cabeçalho)
df = df.drop(df.index[0])
# Renomeando as colunas

df.columns = ['Matricula', 'Nome', 'Unidade do Parceiro', 'Entrada', 'Saída', 'Assinatura', 'Atraso', 'Nota']
df_2.columns = ['Matricula', 'Nome', 'Unidade do Parceiro', 'Entrada', 'Saída', 'Assinatura', 'Atraso', 'Nota']

# concatenando os dois dataframes
alunos = pd.concat([df, df_2],ignore_index=True)

# print(df)
# print(df_2)
print(alunos)

# exportando para csv (para testes)
alunos.to_excel('alunos.xlsx', index=False)

# Todo: 1 - Verificar se a planilha com a presença dos alunos está no formatada
#       2 - Futuramente colocar um laço de repetição para verificar até a ultima planilha da pasta
#       3 - Criar um filtro para verificar se a coluna é NaN e remover a coluna.
