from flask import Flask, jsonify
from flask_cors import CORS

import pdf_functions
import support_functions


app = Flask(__name__)
CORS(app)

# Роут для склеивания файлов PDF
@app.route('/pdfun/api/v1.0/merge_files', methods=['GET'])
def merge_files():
    return jsonify({'Answer': 'file on the position'})

# Роут для отправки кода на вебморду
@app.route('/pdfun/api/v1.0/get_code', methods=['GET'])
def get_code():
    return jsonify({'User_code': support_functions.create_code(4)})

# Роут для авторизации пользователя по коду
@app.route('/pdfun/api/v1.0/auth_from_code', methods=['GET'])
def auth_from_code():
    return jsonify({'User_code': support_functions.create_code(4)})

@app.route('/pdfun/api/v1.0/send_file_to_web', methods=['GET'])
def send_file_to_web():
    pass

@app.route('/pdfun/api/v1.0/del_file', methods=['GET'])
def del_file():
    pass


if __name__ == '__main__':
    app.run(debug=True)