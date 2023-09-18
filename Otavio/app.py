import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from bs4 import BeautifulSoup
import io

app = Flask(__name__)

def extract_data_from_html(file_content):
    soup = BeautifulSoup(file_content, 'html.parser')
    table = soup.find('table')
    table_str = str(table)
    table_io = io.StringIO(table_str)
    df = pd.read_html(table_io, header=0)[0]
    df = df.fillna('')
    return df

def generate_alert_message(df):
    df['Faltas Justificadas'] = df.apply(lambda row: row.str.count('J').sum(), axis=1)
    df['Faltas Não Justificadas'] = df.apply(lambda row: row.str.count('F').sum(), axis=1)
    df['Alerta'] = ''
    df.loc[df['Faltas Justificadas'] == 3, 'Alerta'] = 'Atenção: Três Faltas Justificadas'
    df.loc[df['Faltas Não Justificadas'] >= 3, 'Alerta'] = 'Atenção: Entrar em contato com aluno, possui quatro faltas não justificadas'
    return df

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Nenhum arquivo enviado."
        
        file = request.files['file']
        
        if file:
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            if file_extension == '.xls':
                file_content = file.read()
                df = extract_data_from_html(file_content)
                df_with_alert = generate_alert_message(df)
                table = df_with_alert.to_html(classes='table table-striped')
                
                # Redirecionar para a página de resultado com os dados da tabela
                return redirect(url_for('show_result', table=table))
            else:
                return "Formato de arquivo inválido. Por favor, envie um arquivo .xls."
    
    return render_template('upload.html')

@app.route('/result')
def show_result():
    table = request.args.get('table')  # Obtenha os dados da tabela passados como parâmetro
    return render_template('result.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)
