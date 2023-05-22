from flask import (Flask, render_template, request, flash, session, redirect, url_for, g)
import json
from model import connect_to_db, db, Region
import requests
import os
import crud
# import momentjs
from jinja2 import StrictUndefined

app = Flask(__name__)

app.app_context().push()

app.secret_key = 'dev' 

# app.jinja_env.globals['momentjs'] = momentjs

api_key = os.environ['ALPHAVANTAGE_API_KEY']

app.jinja_env.undefined = StrictUndefined

@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

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

@app.route('/companies')
def companies_by_region():
  
    region_id = request.args.get("region_id")
    
    
    region = Region.query.get(region_id)
    # all_company = crud.get_companies_by_region(region)
    all_company = region.companies

    # import pdb; pdb.set_trace()
    all_company.sort(key = lambda x: x.id )
    return render_template("companies_by_region.html", companies=all_company)
        
@app.route('/company_details')
def view_company_details():
    
    url1 = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey={api_key}'
    overview = requests.get(url1).json()
    # overview_dict = json.loads(overview.text)
    overview_content = {}
    for key, value in overview.items():
        if(key == 'Description'):
            overview_content['Description']=value
        elif(key == 'DividendPerShare'):
            overview_content['DividendPerShare']=value
        elif(key == 'ProfitMargin'):
            overview_content['ProfitMargin']=value
        elif(key == 'QuarterlyEarningsGrowthYOY'):
            overview_content['QuarterlyEarningsGrowthYOY']=value
        elif(key == 'QuarterlyRevenueGrowthYOY'):
            overview_content['QuarterlyRevenueGrowthYOY'] = value
        elif(key == 'AnalystTargetPrice'):
            overview_content['AnalystTargetPrice']=value
        elif(key == '52WeekHigh'):
            overview_content['52WeekHigh'] = value
        elif(key == '52WeekLow'):
            overview_content['52WeekLow']=value
        elif(key == '50DayMovingAverage'):
            overview_content['50DayMovingAverage'] =value
        elif(key == '200DayMovingAverage'):
            overview_content['200DayMovingAverage']=value
        elif(key == 'DividendDate'):
            overview_content['DividendDate']=value
        elif(key == 'ExDividendDate'):
            overview_content['ExDividendDate']=value
   
    url2 = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey={api_key}'
    incomestatements = requests.get(url2).json()
    mrq_incomestatement = incomestatements['quarterlyReports'][0]
    mry_incomestatement = incomestatements['annualReports'][0]
    # quartely_incomestatements = result['quarterlyReports']
    # yearly_incomestatement = result['yearlyReports']


    # incomestatement_dict = json.loads(incomestatement.text)
    # incomestatement_content = {}
    # for i in range(len(incomestatements)):
    #     for key, value in incomestatements[i].items():
    #         if(key == 'fiscalDateEnding'):
    #             incomestatement_content['fiscalDateEnding']=value
    #         elif(key == 'grossProfit'):
    #             incomestatement_content['grossProfit']=value
    #         elif(key == 'totalRevenue'):
    #             incomestatement_content['totalRevenue']=value
    #         elif(key == 'costOfRevenue'):
    #             incomestatement_content['costOfRevenue']=value
    #         elif(key == 'costofGoodsAndServicesSold'):
    #             incomestatement_content['costofGoodsAndServicesSold'] = value
    #         elif(key == 'operatingIncome'):
    #             incomestatement_content['operatingIncome']=value
    #         elif(key == 'researchAndDevelopment'):
    #             incomestatement_content['researchAndDevelopment'] = value
    #         elif(key == 'operatingExpenses'):
    #             incomestatement_content['operatingExpenses']=value
    #         elif(key == 'depreciationAndAmortization'):
    #             incomestatement_content['depreciationAndAmortization'] =value
    #         elif(key == 'incomeBeforeTax'):
    #             incomestatement_content['incomeBeforeTax']=value
    #         elif(key == 'netIncome'):
    #             incomestatement_content['netIncome']=value

    url3 = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey={api_key}'
    balancesheets = requests.get(url3).json()

    mrq_balancesheet = balancesheets['quarterlyReports'][0]
    mry_balancesheet = balancesheets['annualReports'][0]

    return render_template('company_details.html', 
                           overview=overview_content, 
                           mrq_incomestatement=mrq_incomestatement,
                           mry_incomestatement=mry_incomestatement,
                           mrq_balancesheet=mrq_balancesheet,
                           mry_balancesheet=mry_balancesheet
                        )


@app.route('/news')
def news_and_sentiments():
    
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={api_key}'
    result = requests.get(url).json()
    
    news_sentiments = result['feed']
  
    sentiment_score_definition = result['sentiment_score_definition']

    # for news in news_sentiments:
    #     title = news['title']
    #     source = news['url']
    #     authors = news[authors]
    #     summary = news[summary]
    #     time_published = news['time_published']
    #     market_sentiment_score = news['overall_sentiment_score']
    #     market_sentiment_label = news['overall_sentiment_label']
    #     company_specific_sentiment = news['ticker_sentiment']['ticker']
        
    #     ticker_sentiment_score = news['ticker_sentiment']['ticker_sentiment_score']
    #     ticker_sentiment_label = news['ticker_sentiment']['ticker_sentiment_label']

    return render_template("market_news.html", news_sentiments=news_sentiments, sentiment_score_definition=sentiment_score_definition)

@app.route('/gics_sector_tree')
def get_sector_tree():
    return render_template('gics_sectors_tree.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

    