from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug import secure_filename
import os
from db import table_meme

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/imgs')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask('meme')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', memes = table_meme)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file  = request.files['inputFile']

        if file and allowed_file(file.filename):
            filename  = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            dados_dict = request.form.to_dict()
            dados_dict['path'] = 'static/imgs/' + filename
            dados_dict['like'] = 0
            dados_dict['deslike'] = 0
            table_meme.insert(dados_dict)

            file.save(path)
            return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastromeme.html')

@app.route('/like/<id>', methods=['GET'])
def like(id):
    if request.method == 'GET':
        likes = table_meme.find_one(id=id)
        data = dict(id=likes["id"] ,like=likes['like'] + 1)
        table_meme.update(data, ['id'])

        return redirect(url_for('index'))

@app.route('/deslike/<id>', methods=['GET'])
def deslike(id):
    if request.method == 'GET':
        deslikes = table_meme.find_one(id=id)
        data = dict(id=deslikes["id"] ,deslike=deslikes['deslike'] + 1)
        table_meme.update(data, ['id'])

        return redirect(url_for('index'))

@app.route('/apagar/<id>', methods=['GET'])
def delete(id):
    if request.method == 'GET':
        dados_dict = request.form.to_dict()
        table_meme.delete(id=id)

        return redirect(url_for('index'))
