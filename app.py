from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/pdfun/api/v1.0/merge_files', methods=['GET'])
def merge_files():
    return jsonify({'Answer': 'file on the position'})

if __name__ == '__main__':
    app.run(debug=True)