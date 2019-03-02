from flask import Flask
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename
import csv
from flask_bootstrap import Bootstrap
import re
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Expresion regular para verificar numeros
regex = re.compile(r'[0-9]+')
numbers = []
pair = []
odd = []

"""Lee el archivo cvs"""


def read_file(file_name):
    global numbers
    global pair
    global odd
    with open(os.path.join('./uploads/', file_name)) as f:
        reader = csv.reader(f, delimiter=',')
        pair = []
        odd = []
        numbers = [float(item) for sublist in list(reader) for item in sublist if regex.search(item)]
        numbers.sort()
        pair_odd(numbers, pair, odd)


""" Renderiza el Index.html """


@app.route('/')
def index():
    clear()
    return render_template('Index.html')


"""Carga el archivo al directorio uploads"""


@app.route('/data', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename.endswith('.csv'):

            f.save(os.path.join('./uploads/', secure_filename(f.filename)))
            read_file(f.filename)
            return render_template('Data.html', data=numbers, pares=pair, impares=odd)
        else:
            return render_template('Error.html')


""" Verifica que si es par o impar y lo añade a una lista """


def pair_odd(lst, lst_pair, lst_odd):
    for x in lst:
        if x % 2 == 0:
            lst_pair.append(x)
        else:
            lst_odd.append(x)


""" Limpia la lista de pares y la de impares """


def clear():
    pair.clear()
    odd.clear()


if __name__ == "__main__":
    app.run()
