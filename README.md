# Learn2Trade

## Description

This webapp intended to service as an educational and source of information website about publicly traded companies listed on stock exchanges in fourtheen regions or countries (may change on future releases).
The website will allow users to filter or search for a company of their interest, get current stock market related news, access financial fundamentals, mainly balance sheet and income statements of the compnay they are interested in.

## Technologies used

### Language

- Python
- JavaScript
- SQL
- HTML
- CSS

### Frameworks, databases, templates, packages and libraries

- Flask
- flask-paginate
- Flask-SQLAlchemy
- SQLAlchemy
- Bootstrap
- postgreSQL
- Jinja2
- D3
- Werkzeug
- yarl

### API

- AlphaVantage

Learn2Trade is built on a Flask server usign the python programming language and PostgreSQL relational database. SQLAlchemy is used as Obejct Relational Mapper and Jinja2 for html templating.
In addition to CCS Bootstrap, the CSS framework, is used to make the app responsive and to implement some front end styling. D3 is used to build the GICS heirarchical tree map.
The AlphaVantage API, https://stockmarketmba.com/index.php website and Wikipedia used as a data source.

## Features

### Registration/Login

Enen though it is not required to access the content of the webapp, a user may create an account in order to save their searches if they want to save and use it for future reference.  

![User may create a new account or login to their existing account](/static/image/screen-shots/Registration-Login%20page.png).

### Market news

The user is provided with the most recent market news coming from AlphaVantage API and displayed on multiple pages for the user convenience, of course the most recent ones will be on the first page.

![User may create a new account or login to their existing account](/static/image/screen-shots/Market-news.png).

### Market regions

Regional stock market data will be provided, the user may navigate to any region they want to look for companies. Once the user navigated to a specific region, will have access to list of public traded companies
in that region. User may select a specific company and can navigate to the company's fundamentals page.

![User may create a new account or login to their existing account](/static/image/screen-shots/Market%20regions.png).

### GICS Sectors

Displayed a collapsable and expandable d3 hierarchical tree map of Sectors, Industry Groups and Industries. Wikipedia is used as a data source and reference for the classification.

![User may create a new account or login to their existing account](/static/image/screen-shots/GICS%20d3%20tree.png).

### All companies

All companies the webapp provide can be accessed here, the user may use different filtering options to filterdown the data to their interest.  

![User may create a new account or login to their existing account](/static/image/screen-shots/Companies%20page.png).

### Company details

User can have access to the basic company financial fundamentals. specifically balance sheets and income statements.

![User may create a new account or login to their existing account](/static/image/screen-shots/Company%20fundamentals.png). 

## Version 2.0

***More d3 chart:*** Hourly trading market price chart

***Password hashing:*** Password hashing will be implement to protect user's passwords'

***Additional language support:*** Information will be provided with one more additionla language 

## License
