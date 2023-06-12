from flask import (Flask, render_template, request, flash, session, redirect, url_for, g, jsonify)
from model import connect_to_db, db, Region, Company, User_search
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import requests
import os
import re
from datetime import datetime
import datetime as dt
import crud
import random
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args

from jinja2 import StrictUndefined

app = Flask(__name__)
# mod = Blueprint('app', __name__)

app.app_context().push()

app.secret_key = 'dev' 

api_key = os.environ['ALPHAVANTAGE_API_KEY']

app.jinja_env.undefined = StrictUndefined

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

@app.template_filter()
def date_time_format(value):
    year = int(value[:4])
    month = int(value[4:6])
    day = int(value[6:8])
    hour = int(value[9:11])
    minutes = int(value[11:13])

    formatted_date = datetime(year, month, day, hour, minutes)

    # if formatted_date > formatted_date - dt.timedelta(days=8):
    return formatted_date.strftime("%a, %d %b %Y  %H:%M")


@app.route('/')
def homepage():
    """View homepage."""
    return render_template('index.html')

@app.route('/register')
def user_register():
    """View homepage."""
    return render_template('register.html')


@app.route('/register_process', methods=['POST']) 
def user_register_process():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    input_password = request.form.get('password')
    if len(input_password) < 8:
        flash('Password should be eight or more character in length','warning')
        return redirect('/register')
    if crud.get_user_by_email(email) == None :

        user = crud.create_user(fullname, email, input_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account created successfully! You can now login', 'success') 
        return redirect('/login')
    else:
        flash('We have found an account associated with that email. Try again with a different email', 'danger')
    return redirect('/register')

@app.route('/login')
def user_login():
    """View homepage."""
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def user_login_process():
    email = request.form.get('email')
    password =  request.form.get('password')
    user = crud.get_user_by_email(email)

    if not user or user is None:
        flash("We don't find that email in our system, please register or try with a different email address.", "danger")
        return redirect('/login')
    elif user and user.password == password:
        session['user'] = user.id
        if crud.get_saved_searches(user.id):
            flash('Successfuly logged in! Your previous searches have been saved for you, you searched for the following companies in one of your previous sessions.', 'success')
            return redirect('/saved_searches')
        else:
            flash('Successfuly logged in!', 'success')
            return redirect('/')

    else:
        flash("Password don't match, please try again.", "warning")
        return redirect('/login')

@app.route('/logout')
def logout_user():
    session.pop('user', None)
    return render_template('index.html')

@app.route('/regions')
def all_regions():
    
    url = f'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey={api_key}'
    result = requests.get(url).json()

    regions_api = result['markets']
    
    updated_regions = []
    for region in regions_api:
        update_region = crud.get_region_by_name(region['region'])
        if update_region:
            update_region.local_open = region['local_open']
            update_region.local_close = region['local_close']
            update_region.current_status = region['current_status']

            updated_regions.append(update_region)
  
    updated_regions.sort(key = lambda x: x.id )

    return render_template("regions.html", regions=updated_regions)

@app.route('/all_companies')
def get_all_companies():
    all_companies = crud.get_all_companies()

    companies = []
    for company, region, gics_sector, category in all_companies:
        company_detail = {"company_id":company.id,
                          "company_name": company.company_name, 
                          "ticker_symbol":company.ticker_symbol, 
                          "market_capital":company.market_capital, 
                          "region": region.region, 
                          "sector_name": gics_sector.sector_name, 
                          "category": category.category}
        companies.append(company_detail)


    return render_template("all_companies.html", 
                           companies=companies)
# table_data
@app.route('/companies')
def companies_by_region():
    
    region_id = request.args.get("region_id")
    region = Region.query.get(region_id)
    all_company = region.companies

    # import pdb; pdb.set_trace()
    all_company.sort(key = lambda x: x.id )
    return render_template("companies_by_region.html", companies=all_company)

@app.route('/gics_sector_tree')
def get_sector_tree():
    return render_template('gics_sectors_tree.html')

@app.route('/company_details')
def view_company_details():
    company_id = request.args.get("company_id")
    company = crud.get_company_by_id(company_id)
    name = company.company_name
    url1 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company.ticker_symbol}&apikey={api_key}'
    overview = requests.get(url1).json()
    overview_content = {}
    if overview:
      
        for key, value in overview.items():

            key = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', key)
            overview_content[key] = value
    else:
        overview_content = "No company overview is found for "+company.company_name
   
    url2 = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={company.ticker_symbol}&apikey={api_key}'
    incomestatements = requests.get(url2).json()
    mry_incomestatement_modified = {}
    mrq_incomestatement_modified = {}
    if incomestatements:
        
        mrq_incomestatement = incomestatements['quarterlyReports'][0]

        for key, value in mrq_incomestatement.items():
            key = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', key)
            mrq_incomestatement_modified[key] = value
        
        mry_incomestatement = incomestatements['annualReports'][0]
        for key, value in mry_incomestatement.items():
            key = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', key)  
            mry_incomestatement_modified[key] = value  
    else:
        mrq_incomestatement_modified = "No quarterly report has been found for "+company.company_name
        mry_incomestatement_modified = "No annual report has been found for "+company.company_name
   
    url3 = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={company.ticker_symbol}&apikey={api_key}'
    balancesheets = requests.get(url3).json()

    mrq_balancesheet_modified = {}
    mry_balancesheet_modified = {}
    if balancesheets:
        mrq_balancesheet = balancesheets['quarterlyReports'][0]
        for key, value in mrq_balancesheet.items():
            key = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', key)  
            mrq_balancesheet_modified[key] = value  

        mry_balancesheet = balancesheets['annualReports'][0] 
        for key, value in mry_balancesheet.items():
            key = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', key)  
            mry_balancesheet_modified[key] = value  
    else:
        mry_balancesheet_modified = "No annual report has been found for "+company.company_name
        mrq_balancesheet_modified = "No quarterly report has been found for "+company.company_name

    return render_template('company_details.html', 
                           overview=overview_content, 
                           mrq_incomestatement=mrq_incomestatement_modified,
                           mry_incomestatement=mry_incomestatement_modified,
                           mrq_balancesheet=mrq_balancesheet_modified,
                           mry_balancesheet=mry_balancesheet_modified,
                           company_name = name
                        )

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN","NVDA", "BRK-A","META","TSLA","TSM","V","UNH","XOM","JNJ","LLY","WMT","JPM","MA","PG",
"CVX","HD","MRK","AVGO","NVO","ORCL","KO","ASML","PEP","ABBV","AZN","BAC","PFE","COST","BABA","NVS","MCD","CRM","CSCO",
"TMO","TM","ACN","ABT","AMD","LIN","TMUS","DHR","ADBE","CMCSA","NKE","NFLX","DIS"]

ticker = random.choice(tickers)

# The function below constructed for pagination
def get_pagination(page, per_page, total_items):
    pagination = Pagination(page=page, per_page=per_page, total=total_items, css_framework='bootstrap5.2')
    return pagination

@app.route('/news')
def news_and_sentiments():
    company_id = request.args.get("company_id")

    if company_id == None:
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}'
    else: 
        company = crud.get_company_by_id(company_id)
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={company.ticker_symbol}&apikey={api_key}'

    result = requests.get(url).json()
    
    news_sentiments = result['feed']
  
    sentiment_score_definition = result['sentiment_score_definition']

    page = request.args.get('page', type=int, default=1)
    per_page = 6  # Number of items per page
   
    total_items = len(news_sentiments)
    pagination = get_pagination(page, per_page, total_items)
    start = (page - 1) * per_page
    end = start + per_page

    table_data = news_sentiments[start:end]
    
    return render_template("market_news.html", news_sentiments=table_data, pagination=pagination, sentiment_score_definition=sentiment_score_definition)

@app.route('/user_search', methods=['POST'])
def user_search():

    if 'user' in session:

        user_id = session['user']
        company_id = request.json.get('company_id')
        filter = request.json.get('input')

        user_search = crud.create_user_search(user_id, company_id, filter, company_name, ticker_symbol, region, sector_name)
        if user_search:
            db.session.add(user_search)
            db.session.commit()
            return "User search saved successfully!"
    return "search wasn't saved"

@app.route('/saved_searches')
def saved_searches():

    if 'user' in session:
        user_id = session['user']
        saved_user_searches = crud.get_saved_searches(user_id)

    if saved_user_searches:
        return render_template('saved_searches.html', searches = saved_user_searches)
    else:
        return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

    