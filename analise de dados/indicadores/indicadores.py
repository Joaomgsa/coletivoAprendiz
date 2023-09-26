from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


def read_excel():
    df = pd.read_excel('./documentos/apuracao_agosto.xlsx')
    return df

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/indicadores')
def indicadores():
    df = read_excel()
    table = df.to_html(classes='table table-striped table-hover table-sm table-responsive')
    return render_template('indicadores.html', table=table)

@app.route('/acompanhamentoErros')
def formularioerros():
    return render_template('acompanhamentoErros.html')

if __name__ == '__main__':
    app.run(debug=True)