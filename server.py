from flask import (Flask, render_template, request, flash, session, redirect, url_for, g, jsonify)
import json
from model import connect_to_db, db, Region
import requests
import os
from datetime import datetime 
import datetime as dt
import re
import crud
import random
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
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
    if formatted_date >= datetime.today() - dt.timedelta(days=3):
        formatted_date = formatted_date
    # print("##############################################")
        return formatted_date.strftime("%a, %d %b %Y  %H:%M")
    
@app.route('/')
def homepage():
    """View homepage."""
    return render_template('index.html')

@app.route('/search')
def make_global_search():
   
    # search_query = request.args.get('search_query')
    search_query = "New"
    if search_query:
        search_results = crud.get_search_company(search_query)

        search_result_list = []
        for search_result in search_results:
            search_company = {"company_name": search_result.company_name, "ticker_symbol":search_result.ticker_symbol, "market_capital":search_result.market_capital }
            search_result_list.append(search_company)
        # search_results
        # print(search_result_list)
        # return jsonify(search_result_list)
        return render_template('search_result.html', search_results=search_result_list)
   
    
@app.route('/regional_search')
def make_regional_search():
    pass

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
  
    print( email)
    if user and user.password == password:
        session['user'] = user.id
        flash('Logged in!', 'success')
    return redirect('/')


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
ROWS_PER_PAGE = 100
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

    # print(companies['info'])
    return render_template("all_companies.html", companies = companies)

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
   
    url1 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={company.ticker_symbol}&apikey={api_key}'
    overview = requests.get(url1).json()
    if overview:
        overview=overview
    else:
        overview = "No company overview is found for "+company.company_name
    # overview_dict = json.loads(overview.text)
    # ==================================================

    # overview_content = {}
    # for key, value in overview.items():
    #     res_list = []
    #     if re.match('\w*[A-Z][A-Z]\w+', key):
    #         overview_content[key]=value
    #     else:
    #         res_list = re.findall('[A-Z][^A-Z]*', key)
    #         res_list = ' '.join(res_list)
    #         overview_content[res_list.capitalize()] = value

    #======================================================
    #      if(key == 'Description'):
    #         overview_content['Description']=value
    #     elif(key == 'DividendPerShare'):
    #         overview_content['DividendPerShare']=value
    #     elif(key == 'ProfitMargin'):
    #         overview_content['ProfitMargin']=value
    #     elif(key == 'QuarterlyEarningsGrowthYOY'):
    #         overview_content['QuarterlyEarningsGrowthYOY']=value
    #     elif(key == 'QuarterlyRevenueGrowthYOY'):
    #         overview_content['QuarterlyRevenueGrowthYOY'] = value
    #     elif(key == 'AnalystTargetPrice'):
    #         overview_content['AnalystTargetPrice']=value
    #     elif(key == '52WeekHigh'):
    #         overview_content['52WeekHigh'] = value
    #     elif(key == '52WeekLow'):
    #         overview_content['52WeekLow']=value
    #     elif(key == '50DayMovingAverage'):
    #         overview_content['50DayMovingAverage'] =value
    #     elif(key == '200DayMovingAverage'):
    #         overview_content['200DayMovingAverage']=value
    #     elif(key == 'DividendDate'):
    #         overview_content['DividendDate']=value
    #     elif(key == 'ExDividendDate'):
    #         overview_content['ExDividendDate']=value
   
    url2 = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={company.ticker_symbol}&apikey={api_key}'
    incomestatements = requests.get(url2).json()

    if incomestatements:
        
        mrq_incomestatement = incomestatements['quarterlyReports'][0]
        mry_incomestatement = incomestatements['annualReports'][0]
    else:
        mrq_incomestatement = "No quarterly report has been found for "+company.company_name
        mry_incomestatement = "No annual report has been found for "+company.company_name
   
    url3 = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={company.ticker_symbol}&apikey={api_key}'
    balancesheets = requests.get(url3).json()

    if balancesheets:
        mrq_balancesheet = balancesheets['quarterlyReports'][0]
        mry_balancesheet = balancesheets['annualReports'][0] 
    else:
        mry_balancesheet = "No annual report has been found for "+company.company_name
        mrq_balancesheet = "No quarterly report has been found for "+company.company_name

    return render_template('company_details.html', 
                           overview=overview, 
                           mrq_incomestatement=mrq_incomestatement,
                           mry_incomestatement=mry_incomestatement,
                           mrq_balancesheet=mrq_balancesheet,
                           mry_balancesheet=mry_balancesheet
                        )
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN","NVDA", "BRK-A","META","TSLA","TSM","V","UNH","XOM","JNJ","LLY","WMT","JPM","MA","PG",
"CVX","HD","MRK","AVGO","NVO","ORCL","KO","ASML","PEP","ABBV","AZN","BAC","PFE","COST","BABA","NVS","MCD","CRM","CSCO",
"TMO","TM","ACN","ABT","AMD","LIN","TMUS","DHR","ADBE","CMCSA","NKE","NFLX","DIS"]

ticker = random.choice(tickers)

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
   
    return render_template("market_news.html", news_sentiments=news_sentiments, sentiment_score_definition=sentiment_score_definition)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

    