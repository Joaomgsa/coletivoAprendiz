
import pandas as pd

# Lê o arquivo de presença
file = 'presenca.xlsx'

# Lê a planilha de presença
planilha1 = pd.read_excel(file, sheet_name='Folha1')

print(planilha1)