from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)


def read_excel():
    df_faltas = pd.read_excel('./documentos/apuracao_agosto.xlsx')
    #tratamento da coluna de faltas
    df_faltas['Faltas'] = df_faltas['Faltas'].apply(lambda x: '{:.2%}'.format(x))
    # Removendo colunas desnecessárias
    df_faltas.drop(['Total Presenças', 'Presença'], axis=1, inplace=True)
    # Removendo alunos sem faltas 
    df_faltas= df_faltas[df_faltas['Faltas'] != '0.00%']
    # Ordenando por faltas
    #df_faltas.sort_values(by=['Faltas'], ascending=False, inplace=True)
    return df_faltas

def read_excel_alertas():
    df_alertas = pd.read_excel('./documentos/apuracao_agosto.xlsx')
    #tratamento da coluna de faltas
    df_alertas['Faltas'] = df_alertas['Faltas'].apply(lambda x: '{:.2%}'.format(x))
    # Removendo colunas desnecessárias
    df_alertas.drop(['Total Presenças', 'Presença'], axis=1, inplace=True)
    # Removendo alunos sem faltas 
    df_alertas = df_alertas[df_alertas['Faltas'] != '0.00%']
    # Ordenando por faltas
    df_alertas.sort_values(by=['Total Faltas'], ascending=False, inplace=True)
    # Alunos com duas ou mais faltas
    df_alertas = df_alertas[df_alertas['Total Faltas'] >= 2]
    # Removendo colunas desnecessárias
    df_alertas.drop(['Total Faltas','Total de Registros', 'Faltas'], axis=1, inplace=True)
    return df_alertas

def montar_info_alunos():
    #df_base_alunos = pd.read_excel('./documentos/ListaAtivosTurma-92023.xlsx')
    #df_info_alunos.to_excel('./documentos/info_alunos.xlsx', index=False)
    df = pd.read_excel('./documentos/ListaAtivosTurma-92023.xlsx')
    df_base= df[['Apr_Codigo','Apr_Nome','Apr_Celular','Apr_Email']]
    # Removendo duplicados
    df_base.drop_duplicates(subset=['Apr_Codigo'], keep='first', inplace=True)
    # converter coluna para string
    df_base['Apr_Celular'] = df_base['Apr_Celular'].astype(str)
    return df_base

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/indicadores')
def indicadores():
    df_faltas = read_excel()
     # renomear colunas
    df_faltas.rename(columns={'Apr_Codigo': 'Matrícula', 'Apr_Nome_x': 'Nome', 'Total Faltas': 'Faltas', 'Faltas': 'Percent. Faltas'}, inplace=True)
    table_faltas = df_faltas.to_html(classes='table table-striped table-hover table-sm table-responsive', index=False)
    return render_template('indicadores.html', table=table_faltas)

@app.route('/formularioerros')
def formularioerros():
    return render_template('formularioerros.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/alertas')
def alertas():
    df_alertas = read_excel_alertas()
    df_info_alunos = montar_info_alunos()
    df_alertas = pd.merge(df_alertas, df_info_alunos, on='Apr_Codigo', how='left')
    df_alertas = df_alertas[['Apr_Codigo','Apr_Nome_x','Apr_Celular','Apr_Email']]
    # substuir valores nulos pelo valor pesquisar
    df_alertas['Apr_Celular'].fillna('Aluno Sem contatos', inplace=True)
    df_alertas['Apr_Email'].fillna('Aluno Sem contatos', inplace=True)
    # remover caracteres ".0" da coluna celular
    df_alertas['Apr_Celular'] = df_alertas['Apr_Celular'].astype(str).str.replace('.0', '')
    # ordenar por nome
    df_alertas.sort_values(by=['Apr_Nome_x'], ascending=True, inplace=True)
    # renomear colunas
    df_alertas.rename(columns={'Apr_Codigo': 'Matrícula', 'Apr_Nome_x': 'Nome', 'Apr_Celular': 'Celular', 'Apr_Email': 'Email'}, inplace=True)
    #Gerar HTML da tabela
    table_alertas = df_alertas.to_html(classes='table table-striped table-hover table-sm table-responsive', index=False)
    return render_template('alertas.html', table=table_alertas)

@app.route('/notificacoes')
def notificacoes():
    df_alertas = read_excel_alertas()
    df_info_alunos = montar_info_alunos()
    df_alertas = pd.merge(df_alertas, df_info_alunos, on='Apr_Codigo', how='left')
    df_alertas = df_alertas[['Apr_Codigo','Apr_Nome_x','Apr_Celular','Apr_Email']]
    # substuir valores nulos pelo valor pesquisar
    df_alertas['Apr_Celular'].fillna('Aluno Sem contatos', inplace=True)
    df_alertas['Apr_Email'].fillna('Aluno Sem contatos', inplace=True)
    # remover caracteres ".0" da coluna celular
    df_alertas['Apr_Celular'] = df_alertas['Apr_Celular'].astype(str).str.replace('.0', '')
    # ordenar por nome
    df_alertas.sort_values(by=['Apr_Nome_x'], ascending=True, inplace=True)
    # renomear colunas
    df_alertas.rename(columns={'Apr_Codigo': 'Matrícula', 'Apr_Nome_x': 'Nome', 'Apr_Celular': 'Celular', 'Apr_Email': 'Email'}, inplace=True)
    #Gerar HTML da tabela
     #df_alertas.to_html(classes='table table-striped table-hover table-sm table-responsive', index=False)
    return render_template('notificacoes.html',df_alertas=df_alertas)




if __name__ == '__main__':
    app.run(debug=True)