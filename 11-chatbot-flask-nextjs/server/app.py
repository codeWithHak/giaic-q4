from flask import Flask, jsonify
from flask_cors import  CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/home')
def home():
    return jsonify({
        "message":"hello from server"
    })
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
# 1- change port, 2- remove app.run() and play with it, 3- play with CORS, 4- play with jsonify 