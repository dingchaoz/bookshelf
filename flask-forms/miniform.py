# miniform.py
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

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

        return render_template('hello.html', form=form)

    @app.route("/upload_pictures", methods=['GET', 'POST'])
    def upload():
        return(render_template('upload_pictures.html'))

    @app.route("/recommend", methods=['GET', 'POST'])
    def recommend():
        return(render_template('recommend.html'))

    @app.route("/home",methods=['GET', 'POST'] )
    def home():
        return(render_template('hello.html'))


if __name__ == "__main__":
    app.run()
