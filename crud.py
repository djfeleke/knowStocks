"""CRUD operations."""
from model import db, User_search, User, Income_statement, News_and_sentiments, Company_overview, Company,Category_by_capital, Region, GICS_sector, connect_to_db
from sqlalchemy.orm import joinedload, sessionmaker
from datetime import datetime
def create_gics_sector(id, sector_name):
    """Create and return a new gics_sector."""

    gics_sector = GICS_sector(id=id, sector_name=sector_name)
    return gics_sector

def get_all_gics_sectors():
    """ Return all gics_sectors. """
    return GICS_sector.query.all()

def get_gics_sector_by_id(id):
    """ Return gics_sectors name in search """
    return GICS_sector.query.get(id)

def get_gics_sector_by_name(sector_name):
    """ Return gics_sectors name in search """
    return GICS_sector.query.filter(GICS_sector.sector_name==sector_name).all()


def create_region(id, market_type, region, primary_exchanges, local_open, local_close, current_status, notes):
    
    """Create and return a new region/country."""
    region = Region(id=id, market_type=market_type, region=region, primary_exchanges=primary_exchanges,local_open=local_open, local_close=local_close, current_status=current_status, notes=notes)
    return region

def get_all_regions():
    """ Return all existing market regions/countries. """
    return Region.query.all()

def get_region_by_id(id):
    """ Return specific market region based on provided seach id. """
    return Region.query.get(id)

def get_region_by_name(name):
    """ Return specific market region based on provided seach name. """
    return Region.query.filter(Region.region==name).first() #If not running change all() to first()

def get_region_by_market_status(current_status):
    """ Return specific market region based on provided market status. """
    return Region.query.filter(Region.current_status == current_status)

def create_category_by_capital(id, category, description, lower_end, upper_end):
    """Create and return a new category by companies market capital."""
    category_by_capital = Category_by_capital(id=id, category=category, description=description, lower_end=lower_end, upper_end=upper_end)
    return category_by_capital

def get_all_capital_categories():
    """ Return all existing market capital_categories. """
    return Category_by_capital.query.all()

def get_capital_category_by_id(id):
    return Category_by_capital.query.get(id)

def get_capital_category(category):
    return Category_by_capital.query.filter(Category_by_capital.category==category)

def create_company(id,
                    company_name,
                    ticker_symbol, 
                    gics_sector_id,
                    market_capital,
                    region_id,
                    category_by_capital_id):
    """ Create and return a new company. """

    company = Company(id=id, 
                        company_name=company_name,
                        ticker_symbol=ticker_symbol, 
                        gics_sector_id=gics_sector_id,
                        market_capital=market_capital,
                        region_id=region_id,
                        category_by_capital_id=category_by_capital_id)
    return company


def get_all_companies():
    """ Return all existing companies. """
  
    all_companies = db.session.query(Company, Region, GICS_sector, 
                                     Category_by_capital).select_from(Company).join(Region).join(GICS_sector
                                     ).join(Category_by_capital).all()
    
    return all_companies
def get_companies_by_region(region):
    companies_by_region = db.session.query(Company.company_name, Region.region).join(Region).all()
    
    companies_in_region = []
    # import pdb; pdb.set_trace()
    for i, company in enumerate(companies_by_region):
        if(company[i][1] == region.region):
            companies_by_region.append(company)

    return companies_in_region

def get_company_by_id(id):
    return Company.query.get(id)

def get_company_by_ticker_symbol(ticker_symbol):
    return Company.query.filter(Company.ticker_symbol==ticker_symbol)

def get_company_by_name(name):
    return Company.query.filter(Company.company_name==name)

def create_company_overview(company_id,
                            description, 
                            dividend_per_share,
                            profit_margin,
                            quarterly_earnings_growth_YOY,
                            quarterly_revenue_growth_YOY,
                            analyst_target_price,
                            fifty_two_week_high, 
                            fifty_two_week_low,
                            fifty_day_moving_average,
                            two_hundred_day_moving_average,
                            dividend_date,
                            ex_dividend_date,
                            created_date):
    company_overview = Company_overview(company_id = company_id,
                            description = description,
                            dividend_per_share=dividend_per_share,
                            profit_margin=profit_margin,
                            quarterly_earnings_growth_YOY=quarterly_earnings_growth_YOY,
                            quarterly_revenue_growth_YOY=quarterly_revenue_growth_YOY,
                            analyst_target_price=analyst_target_price,
                            fifty_two_week_high=fifty_two_week_high, 
                            fifty_two_week_low=fifty_two_week_low,
                            fifty_day_moving_average=fifty_day_moving_average,
                            two_hundred_day_moving_average=two_hundred_day_moving_average,
                            dividend_date=dividend_date,
                            ex_dividend_date=ex_dividend_date,
                            created_date=created_date)

    return company_overview

def get_company_overview_by_company_id(company_id):
    company_overview = Company_overview.query.filter(Company.company_id==company_id)
    return company_overview

def create_news_and_sentiments(company_id, 
                               title, 
                               source_url, 
                               time_published, 
                               author, 
                               summary, 
                               overall_sentiment_score, 
                               overall_sentiment_label, 
                               ticker_sentiment,
                                created_date):
    news_and_sentiments = News_and_sentiments(company_id, 
                                            title=title, 
                                            source_url=source_url, 
                                            time_published = time_published, 
                                            author = author, 
                                            summary = summary,
                                            overall_sentiment_score=overall_sentiment_score,  
                                            overall_sentiment_label=overall_sentiment_label, 
                                            ticker_sentiment=ticker_sentiment, 
                                            created_date=created_date)

    return news_and_sentiments

def get_news_and_sentiments_by_company_id(company_id):
    news_by_company_id = Company_overview.query.filter(Company.company_id==company_id)
    return news_by_company_id

def get_news_and_sentiments_by_title(title):
    news_by_title = Company_overview.query.filter(Company.title==title)
    return news_by_title

def create_income_statement(company_id,
                            gross_profit,
                            total_revenue,
                            cost_of_revenue,
                            cost_of_goods_and_services,
                            operating_income,
                            research_and_development,
                            operating_expenses,
                            depreciation_and_amortization,
                            income_before_tax,
                            net_income,
                            created_date):
    income_statement = Income_statement(company_id=company_id,
                                        gross_profit=gross_profit,
                                        total_revenue=total_revenue,
                                        cost_of_revenue=cost_of_revenue,
                                        cost_of_goods_and_services=cost_of_goods_and_services,
                                        operating_income=operating_income,
                                        research_and_development=research_and_development,
                                        operating_expenses=operating_expenses,
                                        depreciation_and_amortization=depreciation_and_amortization,
                                        income_before_tax=income_before_tax,
                                        net_income=net_income,
                                        created_date=created_date)
    return income_statement

def get_income_statement_by_company_id(company_id):
    income_statement_bi_company_id = Income_statement.query.filter(Company.company_id==company_id)
    return income_statement_bi_company_id


def create_user(fullname, email, password):
    """Create and return a new user."""

    user = User(fullname=fullname, email=email, password=password)
    return user

def get_all_users():
    """ Return all existing users. """
    return User.query.all()

def get_user_by_id(id):
    return User.query.get(id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def create_user_search(user_id, company_id, search_query):
    user_search = User_search(search_query=search_query, user_id=user_id, company_id=company_id, search_time=datetime.now())
    return user_search

def get_saved_searches(user_id):
    # results = User_search.query.filter(User_search.user_id == user_id).order_by(User_search.timestamp.desc()).all()

    return User_search.query.filter(User_search.user_id==user_id).order_by(User_search.search_time.desc()).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)