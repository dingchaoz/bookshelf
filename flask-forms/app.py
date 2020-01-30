# import the Flask Class from the flask module

from flask import Flask, render_template

# create application object

app = Flask (__name__)

# use decorators to link the function to a url

@app.route('/')
def home():
    return "test"

@app.route('/welcome')
def welcome():
  return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
