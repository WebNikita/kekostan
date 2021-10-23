from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/pdfun/api/v1.0/merge_files', methods=['GET'])
def merge_files():
    return jsonify({'Answer': 'file on the position'})

if __name__ == '__main__':
    app.run(debug=True)