from flask import Flask, jsonify, request, session, send_from_directory
from flask.helpers import send_file
from flask.wrappers import Request
import requests
from flask_cors import CORS
import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

import pdf_functions
from support_functions import save_files, create_code

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
    
    if os.path.isfile('./users_files/test.pdf'):
        os.remove('./users_files/test.pdf')
    path_bufer = []
    for filepath in save_files(request):
        path_bufer.append(filepath)
    pdf_functions.merge_files(path_bufer, "./users_files/test.pdf")
    return send_from_directory("./users_files/", "test.pdf", as_attachment=True)


# Роут для отправки кода на вебморду
@app.route("/pdfun/api/v1.0/get_code", methods=["GET"])
def get_code():
    user_code = create_code(99, 999)
    user = Users(key=user_code)
    session.add(user)
    session.commit()
    return jsonify({"user_code": user_code})


# Роут для авторизации пользователя по коду
@app.route("/pdfun/api/v1.0/auth_from_code", methods=["POST"])
def auth_from_code():
    data_code = request.json
    print(data_code.get("code"))
    if session.query(Users).filter_by(key=data_code.get("code")).first():
        return jsonify({"status": True})
    else:
        return jsonify({"status": False})


@app.route("/pdfun/api/v1.0/get_file_from_tg", methods=["POST"])
def send_file_to_web():
    import json

    payload = request.data.decode("utf-8")
    user_code = json.loads(payload)["user_code"]
    try:
        print(user_code)
        if os.path.isdir(f'./users_files/{user_code}'):
            print(os.listdir(f'./user_files/{user_code}'))
            # return json.dumps({'file_path': []})
    except Exception as e:
        print("Something goes wrong " + str(e))
    return str(payload)
@app.route("/pdfun/api/v1.0/save_file_from_tg", methods=["POST"])
def save_file_from_tg():
    data_files = request.files.lists()
    files_bufer = {}
    print(request.files)
    # print(data_files)
    counter = 0
    for data in data_files:
        print(data[1])
        file_name = secure_filename(data[1][0].filename)
        if not os.path.isdir(f'./users_files/{data[0]}'):
            os.mkdir(f'./users_files/{data[0]}')
        data[1][0].save(f"./users_files/{data[0]}/{file_name}")
    return 'ok'

@app.route("/pdfun/api/v1.0/flip_pages", methods=["POST"])
def flip_pages():
    for filepath in save_files(request):
        pdf_functions.flip_pages(filepath)
    shutil.make_archive(
        f"./users_files/rotated",
        "zip",
        f"./users_files/rotated",
    )
    shutil.rmtree("./users_files/rotated")
    return send_from_directory("./users_files/", f"rotated.zip", as_attachment=True)


@app.route("/pdfun/api/v1.0/split_pages", methods=["POST"])
def split_pages():
    for filepath in save_files(request):
        print(filepath)
        pdf_functions.split_pages(filepath)
    fname = os.path.basename(filepath).split(".")[0]
    print("fname" + fname)
    shutil.make_archive(
        f"./users_files/{fname}",
        "zip",
        f"./users_files/{fname}",
    )
    shutil.rmtree(f"./users_files/{fname}")
    return send_from_directory("./users_files/", f"{fname}.zip", as_attachment=True)



@app.route("/pdfun/api/v1.0/del_file", methods=["POST"])
def del_file():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=8001)
