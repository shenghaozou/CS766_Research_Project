from flask import Flask
from flask import request
import base64
import subprocess
app = Flask(__name__)

COMMAND = ['python', 'inference.py', '--image', './test.png', '--restore_checkpoints', 'Models/SVHN/tensorflow_model/model.ckpt-328000']

@app.route('/')
def hello_world():
    return 'Server is running!'

@app.route('/detect', methods = ['POST'])
def detect():
    if request.method == 'POST':
        data = request.form['data']
        d = base64.b64decode(data)
        with open('test.png', 'wb') as fw:
            fw.write(d)
        result = subprocess.run(COMMAND, stdout=subprocess.PIPE)
        return 'STDOUT:\n{}\nSTDERR:\n'.format(result.stdout.decode('utf-8') if result.stdout else '', result.stderr.decode('utf-8') if result.stderr else '')
