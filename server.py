from flask import (Flask, render_template, request, flash, session, redirect, url_for)
from model import connect_to_db, db
import requests
import os
import crud
from jinja2 import StrictUndefined

# def create_app():
#     app = Flask(__name__)
#     db.init_app(app)
#     return app
app = Flask(__name__)

app.app_context().push()

app.secret_key = 'dev'

api_key = os.environ['ALPHAVANTAGE_API_KEY']

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('index.html')

@app.route('/search')
def make_search():

    search_query = request.args.get('search_query')
    if search_query:
        search_results = crud.get_search_company(search_query)
        return render_template('search_filters.html', search_results=search_results)

@app.route('/login')
def user_login():
    """View homepage."""
    return render_template('login.html')

@app.route('/register')
def user_register():
    """View homepage."""
    return render_template('register.html')


@app.route('/register_process', methods=['POST']) 
def user_register_process():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')

    print(fullname, email, password, cpassword)
    print(crud.get_user_by_email(email))
    if crud.get_user_by_email(email) == None:
        user = crud.create_user(fullname, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Your account created successfully! You can now login')
    else:
        flash('We have found an account associated with that email. Try again with a different email')
    return redirect('/')


@app.route('/login_process', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password =  request.form.get('password')

    user = crud.get_user_by_email(email)
    if user and user.password == password:
        session['id'] = user.id
        flash('Logged in!')
    return redirect('/')


@app.route('/regions')
def all_regions():
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
    result = requests.get(url).json()
    print(result)
    regions = crud.get_all_regions()

    return render_template("regions.html", regions_api = result['markets'], regions=regions)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)