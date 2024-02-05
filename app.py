from flask import Flask, request, render_template
import zipfile
import os
import io

app = Flask(__name__)

def extract_zip_content(zip_file):
    content_list = []
    with zipfile.ZipFile(zip_file, 'r') as zip_data:
        for file_info in zip_data.infolist():
            with zip_data.open(file_info) as f:
                content_list.append(f.read().decode('utf-8'))
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

            # Obtener el contenido del archivo ZIP
            content_list = extract_zip_content(temp_path)

            # Eliminar el archivo temporal después de obtener el contenido
            os.remove(temp_path)

            return render_template('index.html', content_list=content_list)
        else:
            return render_template('index.html', error='El archivo no es un archivo ZIP válido')

    return render_template('index.html')

@app.route('/delete', methods=['POST'])
def delete_files():
    # Eliminar archivos según tus necesidades
    # Puedes modificar esta función para adaptarla a tu lógica específica
    return render_template('index.html', message='Archivos eliminados exitosamente')

if __name__ == '__main__':
    app.run(debug=True)
