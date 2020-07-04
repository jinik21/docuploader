import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import psycopg2
from sqlalchemy.orm.attributes import flag_modified
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','doc'}

app = Flask(__name__)
app.secret_key="12345678"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='postgres://cuxjgdflxrmpva:f94003ed77322cc3761fc226363edb2d2cf00647211af1e522f4f80c1dc742b0@ec2-34-230-231-71.compute-1.amazonaws.com:5432/d41m4e6re5dv5a'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db=SQLAlchemy(app)
users=db.Table('users',db.metadata,autoload=True,autoload_with=db.engine,extend_existing=True)

class users(db.Model):
    _tablename_='users'
    __table_args__ = {'extend_existing': True} 
    id=db.Column('id',db.Integer,primary_key=True)
    usernum=db.Column('usernum',db.Integer)
    entries=db.Column('entries',db.Integer)
    def _init_(self,id,usernum,entreis):
        self.id=id
        self.usernum=usernum
        self.entries=entries

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
entries=0
loc=''
file=''
entriesg=0
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global entries
    global loc
    global file
    usernum=0
    totentries=db.session.query(users).order_by(desc('id')).first()
    loc=''
    entries=0
    global entriesg
    
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            return render_template('index.html',error='No File PArt',entries=entries,totentries=totentries)
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html',entries=entries,error='No File Selected',totentries=totentries)
        
        if file and allowed_file(file.filename) and entriesg<3:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            entriesg+=1
            useren=db.session.query(users).order_by(desc('id')).first()
            #useren=users(id=totentries.id,usernum=totentries.usernum,entries=totentries.entries+1)
            setattr(useren, 'entries', totentries.entries+1)
            db.session.commit()
            totentries=db.session.query(users).order_by(desc('id')).first()
                
            if entriesg==3 and allowed_file(file.filename):
                abc=render_template('thanku.html',totentries=totentries,loc=loc)
                user=users(usernum=totentries.usernum+1,entries=totentries.entries)
                db.session.add(user)
                db.session.commit()
                loc=''
                entries=0
                entriesg=0
                return abc
            return render_template('index.html',entries=entriesg,totentries=totentries,loc=loc,error='Successfully Uploaded')
        else:
            return render_template('index.html',error='wrong file format(make sure in txt, pdf, png, jpg, jpeg, gif,doc)',entries=entriesg,totentries=totentries,files=file)
    if request.method=='GET':
        user=users(usernum=totentries.usernum+1,entries=totentries.entries)
        db.session.add(user)
        db.session.commit()
    return render_template('index.html',entries=entries,totentries=totentries,loc=loc,files=loc)

if __name__ == "__main__": 
        app.run() 