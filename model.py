from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GICS_sector(db.Model):
    
    __tablename__ = 'gics_sectors'
    id = db.Column(db.Integer,                   
                    primary_key=True)
    sector_name = db.Column(db.String(100), nullable=True,)

    companies = db.relationship('Company', back_populates='gics_sectors')
    
    def __repr__(self):
        return f'<GICS_sector id={self.id} sector_name={self.sector_name}>'

class Region(db.Model):
    
    __tablename__ = 'regions'

    id = db.Column(db.Integer,
                    primary_key=True)
    market_type = db.Column(db.String(100), nullable=False,)
    region = db.Column(db.String(50), nullable=False,)
    primary_exchanges = db.Column(db.String(150), nullable=False,)
    local_open = db.Column(db.String(20), nullable=False,)
    local_close = db.Column(db.String(20), nullable=False,)
    current_status = db.Column(db.String(10), nullable=True,)
    notes = db.Column(db.Text, nullable=True,)
     
    companies = db.relationship('Company', back_populates='regions')
    
    def __repr__(self):
        return f'<Region id={self.id} region={self.region}>'

class Category_by_capital(db.Model):
    
    __tablename__ = 'categories_by_capital'
    
    id = db.Column(db.Integer,
                    primary_key=True)

    category = db.Column(db.String(30))  
    description = db.Column(db.String(150))
    lower_end = db.Column(db.Float)
    upper_end = db.Column(db.Float)
   
    companies = db.relationship('Company', back_populates='categories_by_capital')

    def __repr__(self):
        return f'<Category_by_capital id={self.id} category={self.category}>'

class Company(db.Model):
    
    __tablename__ = 'companies'

    id = db.Column(db.Integer,
                    primary_key=True)
    company_name = db.Column(db.Text, nullable=False,)
    ticker_symbol = db.Column(db.String(20), nullable=False,)
    gics_sector_id = db.Column(db.Integer, db.ForeignKey('gics_sectors.id'))
    market_capital = db.Column(db.BigInteger)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))
    category_by_capital_id = db.Column(db.Integer, db.ForeignKey('categories_by_capital.id'))
   
    categories_by_capital = db.relationship('Category_by_capital', back_populates='companies')
    regions = db.relationship('Region', back_populates='companies')
    gics_sectors = db.relationship('GICS_sector', back_populates='companies')
    
    companies_overviews = db.relationship('Company_overview', back_populates='companies')
    news_and_sentiments = db.relationship('News_and_sentiments', back_populates='companies')
    income_statements = db.relationship('Income_statement', back_populates='companies')
    users_searches = db.relationship('User_search', back_populates='companies')
 
    def __repr__(self):
        return f'<Company id={self.id} company_name={self.company_name}>'

class Company_overview(db.Model):

    __tablename__ = 'companies_overviews'
    id = db.Column(db.Integer, 
                    autoincrement=True,
                    primary_key=True)
    
    description = db.Column(db.Text)
    MarketCapitalization = db.Column(db.String(30))
    dividend_per_share = db.Column(db.Float)
    profit_margin = db.Column(db.Float)
    quarterly_earnings_growth_YOY = db.Column(db.Float)
    quarterly_revenue_growth_YOY = db.Column(db.Float)
    analyst_target_price = db.Column(db.Float)
    fifty_two_week_high = db.Column(db.Float)
    fifty_two_week_low = db.Column(db.Float)
    fifty_day_moving_average = db.Column(db.Float)
    two_hundred_day_moving_average = db.Column(db.Float)
    dividend_date = db.Column(db.Float)
    ex_dividend_date = db.Column(db.Float)
    created_date = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    companies = db.relationship('Company', back_populates='companies_overviews')

    def __repr__(self):
        return f'<Company_overview id={self.id} company_name={self.company_name}>'

class News_and_sentiments(db.Model):

    __tablename__ = 'news_and_sentiments'

    id = db.Column(db.Integer, 
                    autoincrement=True,
                    primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    title = db.Column(db.Text)
    source_url = db.Column(db.Text)
    time_published = db.Column(db.DateTime)
    author = db.Column(db.String(100))
    summary = db.Column(db.Text)
    overall_sentiment_score = db.Column(db.Float)
    overall_sentiment_label = db.Column(db.String)
    ticker_sentiment = db.Column(db.String)
    created_date = db.Column(db.DateTime)

    companies = db.relationship('Company', back_populates='news_and_sentiments')

    def __repr__(self):
        return f'<News_and_sentiments id={self.id} title={self.title}>'

class Income_statement(db.Model):

    __tablename__ = 'income_statements'
    
    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    gross_profit = db.Column(db.Float)
    total_revenue = db.Column(db.Float)
    cost_of_revenue = db.Column(db.Float)
    cost_of_goods_and_services = db.Column(db.Float)
    operating_income = db.Column(db.Float)
    research_and_development = db.Column(db.Float)
    operating_expenses = db.Column(db.Float)
    depreciation_and_amortization = db.Column(db.Float)
    income_before_tax = db.Column(db.Float)
    net_income = db.Column(db.Float)
    created_date = db.Column(db.DateTime)

    companies = db.relationship('Company', back_populates='income_statements')

    def __repr__(self):
        return f'<Income_statement id={self.id} company_id={self.company_id}>'

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, 
                    autoincrement=True,
                    primary_key=True)
    fullname = db.Column(db.String(50), nullable=False,)
    email = db.Column(db.String(30), nullable=False,unique=True,)
    password = db.Column(db.String(15), nullable=False)

    users_searches = db.relationship('User_search', back_populates='users')

    def __repr__(self):
        return f'<User id={self.id} first_name={self.first_name} last_name={self.last_name}>'

class User_search(db.Model):
    
    __tablename__ = 'users_searches'

    id = db.Column(db.Integer, 
                    autoincrement=True,
                    primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    users = db.relationship('User', back_populates='users_searches')
    companies = db.relationship('Company', back_populates='users_searches')

    def __repr__(self):
        return f'<User_search id={self.id} first_name={self.first_name} last_name={self.last_name}>'

def connect_to_db(flask_app, db_uri="postgresql:///stocks", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)