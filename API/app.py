from flask import Flask, jsonify, request, session, send_from_directory
from flask.helpers import send_file
from flask.wrappers import Request
from flask_cors import CORS
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

import pdf_functions
import support_functions

from models import Users, Base


app = Flask(__name__)
CORS(app)

engine = create_engine("sqlite:///main.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Роут для склеивания файлов PDF
@app.route("/pdfun/api/v1.0/merge_files", methods=["POST"])
def merge_files():
    
    if os.path.isfile('/home/pdf/kekostan/API/users_files/test.pdf'):
        os.remove('/home/pdf/kekostan/API/users_files/test.pdf')
    
    path_bufer = []
    data_info = request
    data_files = request.files.lists()
    print(request.files)
    # print(data_files)
    for data in data_files:
        print(data)
        user_code = data[0]
        print(user_code)
        for items in data[1]:
            file_name = secure_filename(items.filename)
            items.save(f"/home/pdf/kekostan/API/users_files/{file_name}")
            path_bufer.append(f"/home/pdf/kekostan/API/users_files/{file_name}")
    pdf_functions.merge_files(path_bufer, "/home/pdf/kekostan/API/users_files/test.pdf")
    return send_from_directory("/home/pdf/kekostan/API
/users_files/", "test.pdf", as_attachment=True)


# Роут для отправки кода на вебморду
@app.route("/pdfun/api/v1.0/get_code", methods=["GET"])
def get_code():
    user_code = support_functions.create_code(99, 999)
    user = Users(key=user_code)
    session.add(user)
    session.commit()
    return jsonify({"user_code": user_code})


# Роут для авторизации пользователя по коду
@app.route("/pdfun/api/v1.0/auth_from_code", methods=["POST"])
def auth_from_code():
    return jsonify({"user_code": 'Ok'})


@app.route("/pdfun/api/v1.0/get_file_from_tg", methods=["POST"])
def send_file_to_web():
    pass


@app.route("/pdfun/api/v1.0/del_file", methods=["POST"])
def del_file():
    pass


if __name__ == "__main__":
    app.run(debug=True)
