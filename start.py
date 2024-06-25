import glob
import os
import warnings
import textract
import requests
from flask import (Flask, g, json, Blueprint, flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from werkzeug.utils import secure_filename

import pdf2txt as pdf
import PyPDF2

import screen
import search
import hashlib


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='Project key',
))

app.config['UPLOAD_FOLDER'] = r'C:\Users\sc941\OneDrive\Desktop\Anti Spoofing\Resumes'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]

@app.route('/')
def home():
    x = []
    for file in glob.glob("./Job_Description/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results=x)

@app.route('/results', methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        jobfile = request.form['des']
        print(jobfile)
        flask_return = screen.res(jobfile)
        print(flask_return)
        return render_template('result.html', results=flask_return)

@app.route('/resultscreen', methods=['POST', 'GET'])
def resultscreen():
    if request.method == 'POST':
        jobfile = request.form.get('Name')
        print(jobfile)
        flask_return = screen.res(jobfile)
        return render_template('result.html', results=flask_return)

@app.route('/resultsearch', methods=['POST', 'GET'])
def resultsearch():
    if request.method == 'POST':
        search_st = request.form.get('Name')
        print(search_st)
    result = search.res(search_st)
    return render_template('result.html', results=result)

@app.route('/Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Resumes', filename)

# Add this function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Add this new route for uploading resumes
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        flash('File successfully uploaded')
        return redirect(url_for('home'))
    else:
        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        return redirect(request.url)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True, threaded=True)
