# miniform.py
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), \
                                            validators.Length(min=6, max = 35)])
    password = TextField('Password:', validators = [validators.required(), \
                                            validators.Length(min=4, max=35)])

# Home page, loads a login button and a registration button
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        password=request.form['password']
        email = request.form['email']

        print(name, " ", email, " ", password)

    if form.validate():
            # comment here
        flash('Thank you for your registration ' + name)

        #if not registering to save file, enter alternate storage options

    else:
        flash('All the form fields are required. ')

    return render_template('index.html', form=form)

# Login Template
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html', form=form)

# after completing registration sends you to an action and verification page
@app.route("/registered", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        name = request.form['name']
    return(render_template('registered.html', form=form))

# Template for uploading pictures
@app.route("/upload_pictures/<string:name>/", methods=['GET', 'POST'])
def upload(name):
    if request.method=='POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        flash("Upload Sucessful!")
    return(render_template('upload_pictures.html/', name=name))

# After uploading pictures, this template directs you to the dashboard
@app.route("/uploaded/", methods=['GET', 'POST'])
def uploaded(name):
    if request.method=='POST':
        f =request.files['file']
        f.save(secure_filename(f.filename))

    return(render_template('uploaded.html/', name=name))

# REcommendation Page
@app.route("/recommend/<string:name>/", methods=['GET', 'POST'])
def recommend(name):
    return(render_template('recommend.html/', name=name

# Session and Cookie Template
@app.route('/save', methods = ["GET","POST"])
def setcookie():
    if request.method == "POST":
        session['user'] = request.form['name']
        resp = make_response(render_template('dashboard.html', name=session['user']))

        return resp

# Dashboard Template
@app.route("/dashboard/<name>",methods=['GET', 'POST'] )
def dash(name):
    return(render_template('dashboard.html', name=name)

# Delete a session Template
@app.route('/delete')
def deleteSession():
    session.pop('user', None)
    return ''

if __name__ == "__main__":
    app.run()
