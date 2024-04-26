from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/diagram')
def diagram():
    return render_template('diagram.html',)


if __name__ == '__main__':
    app.run(debug=True)