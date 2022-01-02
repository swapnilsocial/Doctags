import os
from flask import Flask, render_template, Response, request

app = Flask(__name__)

USER_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Landing Page
@app.route('/tagcloud_template', methods=['POST', 'GET'])
def index():
    return render_template('tagcloud_template.html')

# Landing Page
@app.route('/tagcloud', methods=['POST', 'GET'])
def tagcloud():
    page = '/saved_doctags/tagcloud.html'
    return render_template(page)

#
@app.route('/')
def server_status():
    return "Server is up and running!"


# run flask and expose ip and port
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8030)