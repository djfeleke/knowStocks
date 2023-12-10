import os
import json
from datetime import datetime
from server import app

import crud
import model
import server

# pg_dump stocks > stocks.sql # saving copy of the database schema to a files before dropping the database
os.system("dropdb stocks")
os.system("createdb stocks")
# psql stocks < stokcs.sql # restoring the database schema from a files after recreating the database

model.connect_to_db(server.app)
model.db.create_all()

with open("data/category_by_market_capital.json") as catagories:
    market_capital_category = json.loads(catagories.read())

market_capital_categories_in_db = []
for category in market_capital_category:
    # print(category)
    new_category = crud.create_category_by_capital(category["id"],
                                                    category["category"], 
                                                    category["description"], 
                                                    category["lower_end"], 
                                                    category["upper_end"]  )
            
    market_capital_categories_in_db.append(new_category)

with open("data/regions_list.json") as regions:
    regions_list = json.loads(regions.read())

regions_in_db = []
for region in regions_list:
    new_region = crud.create_region(region["id"],
                                    region["market_type"], 
                                    region["region"],
                                    region["primary_exchanges"], 
                                    region["local_open"], 
                                    region["local_close"], 
                                    region["current_status"],
                                    region["notes"]
                                    )
    regions_in_db.append(new_region)

with open("data/gics_sectors.json") as gics_sectors:
    gics_sectors_list = json.loads(gics_sectors.read())

gics_sectors_in_db = []
for gics_sector in gics_sectors_list:
    new_gics_sector = crud.create_gics_sector(gics_sector["id"], gics_sector["gics_sector"])

    gics_sectors_in_db.append(new_gics_sector)

model.db.session.add_all(market_capital_categories_in_db)
model.db.session.add_all(regions_in_db)
model.db.session.add_all(gics_sectors_in_db)
model.db.session.commit()

with open("data/companies_list.json") as companies:
    companies_list = json.loads(companies.read())

companies_in_db = []
for company in companies_list:
    # print(company)
    new_company = crud.create_company(id=company["id"],
                                        company_name =company["company_name"],
                                        ticker_symbol = company["ticker_symbol"], 
                                        gics_sector_id = company["gics_sector_id"],
                                        market_capital = company["market_capital"],
                                        region_id = company["region_id"],
                                        category_by_capital_id=company["market_cap_categery_id"])
                    
    companies_in_db.append(new_company)

model.db.session.add_all(companies_in_db)
model.db.session.commit()
