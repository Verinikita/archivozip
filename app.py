from flask import Flask, request, render_template
import zipfile
import os
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se ha enviado un archivo
        if 'file' not in request.files:
            return render_template('index.html', error='No se seleccionó ningún archivo')

        file = request.files['file']

        # Verificar si se ha seleccionado un archivo
        if file.filename == '':
            return render_template('index.html', error='No se seleccionó ningún archivo')

        # Verificar si es un archivo ZIP
        if file and file.filename.endswith('.zip'):
            # Descomprimir el archivo
            zip_data = zipfile.ZipFile(file.stream, 'r')
            content_list = []

            for file_info in zip_data.infolist():
                with zip_data.open(file_info) as f:
                    content_list.append(f.read().decode('utf-8'))

            return render_template('index.html', content_list=content_list)
        else:
            return render_template('index.html', error='El archivo no es un archivo ZIP válido')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
