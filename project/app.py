import os
from flask import Flask, redirect, render_template, request, url_for
from server import DocumentAnalysis as DAnalysis 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/input', methods=['GET', 'POST'])
def upload_file():
    message = ''
    if request.method == 'POST':
        diagram_type = request.form.get('diagrams')
        file = request.files['file']
        filename = file.filename
        file_extension = os.path.splitext(filename)[1]
        
        if file_extension in ['.txt', '.pdf']:
            DAnalysis.dataInitialization(file,file_extension,diagram_type)
            return redirect(url_for('diagram'))
        else:
            message = 'Invalid file type. Please upload a .txt or .pdf file.'

        diagram_type = request.form.get('diagrams')
    return render_template('input.html', message=message)


@app.route('/diagram')
def diagram():
    return render_template('diagram.html',)


if __name__ == '__main__':
    app.run(debug=True)