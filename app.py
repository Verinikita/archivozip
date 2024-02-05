from flask import Flask, request, render_template, send_file
import zipfile
import os
import io

app = Flask(__name__)

def get_zip_file_content(zip_file):
    content_list = []
    with zipfile.ZipFile(zip_file, 'r') as zip_data:
        content_list = zip_data.namelist()
    return content_list

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No se seleccionó ningún archivo')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No se seleccionó ningún archivo')

        if file and file.filename.endswith('.zip'):
            # Guardar el archivo temporalmente
            temp_path = 'temp.zip'
            file.save(temp_path)

            # Obtener la lista de archivos en el archivo ZIP
            file_list = get_zip_file_content(temp_path)

            return render_template('index.html', file_list=file_list)
        else:
            return render_template('index.html', error='El archivo no es un archivo ZIP válido')

    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Descargar el archivo seleccionado
    return send_file(filename, as_attachment=True)

@app.route('/delete', methods=['POST'])
def delete_files():
    # Eliminar archivos según tus necesidades
    # Puedes modificar esta función para adaptarla a tu lógica específica
    return render_template('index.html', message='Archivos eliminados exitosamente')

if __name__ == '__main__':
    app.run(debug=True)
