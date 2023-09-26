from flask import Flask, render_template
import pandas as pd

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
    return df_alertas

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/indicadores')
def indicadores():
    df_faltas = read_excel()
    table_faltas = df_faltas.to_html(classes='table table-striped table-hover table-sm table-responsive')
    return render_template('indicadores.html', table=table_faltas)

@app.route('/acompanhamentoErros')
def formularioerros():
    return render_template('acompanhamentoErros.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/alertas')
def alertas():
    df_alertas = read_excel_alertas()
    table_alertas = df_alertas.to_html(classes='table table-striped table-hover table-sm table-responsive')
    return render_template('alertas.html', table=table_alertas)


if __name__ == '__main__':
    app.run(debug=True)