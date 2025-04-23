from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename

app=Flask(__name__)

UPLOAD_FOLDER='uploads'
ALLOWED_EXTENSIONS={'txt','pdf','png','jpg','jpeg','gif','doc','docx','csv','xlsx','zip'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files=os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html',files=files)

@app.route('/upload',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file=request.files['file']
    
    if file.filename=='':
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if os.path.exists(file_path):
        return send_file(file_path,as_attachment=True)
    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
