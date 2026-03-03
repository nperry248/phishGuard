from flask import Flask, jsonify, request
from flask_cors import CORS
from prediction import run

app = Flask(__name__)
CORS(app)  # Allow all origins (required for Chrome extension requests)


@app.route('/', methods=['GET'])
def make_prediction():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing "url" parameter'}), 400

    result = run(url)
    return jsonify({'prediction': result})


if __name__ == '__main__':
    app.run(port=5000)
