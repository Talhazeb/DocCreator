from flask import Flask, request, render_template
from webservice.verification import verify_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Keine Datei hochgeladen', 400
        file = request.files['file']
        if file.filename == '':
            return 'Keine Datei ausgewählt', 400
        if file and file.filename.endswith('.pdf'):
            result = verify_pdf(file)
            return render_template('result.html', result=result)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)

