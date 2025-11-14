from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_data')
def list_data():
    list_data = db.get_all_data()
    return render_template('list_data.html', list_data=list_data)

if __name__ == '__main__':
    app.run(debug=True)