import boto3
import os
from flask import Flask, request, render_template

# S3 Credentials and Connection to the Bucket
s3 = boto3.resource('s3')
my_bucket = 'febatech-web-assets'
bucket = s3.Bucket(my_bucket)
image_extensions = ['jpg', 'png', 'JPG', 'JPEG', 'PNG','txt','TXT','PDF','pdf','log','LOG','py','PY','html','HTML','JSON','json','md','MD','md','csv','CSV']
app = Flask(__name__, static_url_path='/temp', static_folder='temp')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Main Page.
@app.route('/')
def welcome():
    return render_template('login.html')


# Login check whether the user is registered or not from a local text file.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        registered_user_names = open('login.txt', 'r').read().splitlines()
        for name in registered_user_names:
            if name == user_name:
                return render_template('response.html')
    return 'Not a registered User'


# Listing the files from Amazon AWS S3 account
@app.route('/list', methods=['GET', 'POST'])
def list_files():
    if request.method == 'GET':
        value = []
        for objects in bucket.objects.all():
            value.append(objects.key)
        return render_template('response.html', list_objects=value)


# Uploading the files to your AWS S3 account
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        upload_file = request.files['file']
        upload_file_extension = str(upload_file.filename).split('.', 1)[1]
        if upload_file_extension in image_extensions:
            bucket.put_object(Key=upload_file.filename, Body=upload_file)
            msg = "file uploaded"
            return render_template('response.html',msg=msg)
    return 'Not a valid file'


# Downloading the user specified file from AWS S3 using bucket policy
@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        filename = request.form['filename']
        url = "https://febatech-web-assets.s3.ap-south-1.amazonaws.com/"+filename
        return render_template('response.html', url=url)

    return render_template('response.html')


if __name__ == "__main__":
    app.run(debug=True)
