import json
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file

# the "files" directory next to the app.py file
USER_FOLDER = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.dirname(USER_FOLDER + '/uploads/')
print(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def main_page():
    return _show_page()

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    #file = request.files['file']
    app.logger.info(request.files)
    upload_files = request.files.getlist('file')
    app.logger.info(upload_files)
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if not upload_files:
        flash('No selected file')
        return redirect(request.url)
    for file in upload_files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    flash('Upload succeeded')
    return redirect(url_for('upload_file'))


@app.route('/download/<code>', methods=['GET'])
def download(code):
    files = _get_files()
    if code in files:
        path = os.path.join(UPLOAD_FOLDER, code)
        if os.path.exists(path):
            return send_file(path)
    os.abort(404)

def _show_page():
    files = _get_files()
    return render_template('index.html', files=files)

def _get_files():
    file_list = os.path.join(UPLOAD_FOLDER, 'files.json')
    if os.path.exists(file_list):
        with open(file_list) as fh:
            return json.load(fh)
    return {}


# run flask and expose ip and port
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8030)