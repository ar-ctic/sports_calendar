from flask import Flask, request, render_template, jsonify

from models.database import initDatabase

app = Flask(__name__, template_folder='views', static_folder='static')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    
     
    
    initDatabase()
    
    app.run(debug=True, port=5000)