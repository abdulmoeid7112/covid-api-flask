from flask import make_response
from flask import current_app as app
from .models import db, CovidStatsCountry, CovidStatsCountryRegion, CovidStatsUs
import requests

# index Route 
@app.route('/', methods=['GET'])
def index():
    if (db):
        return """
                <h1>Restful API Server</h1>
                <p>Collects data and stores it in a database for covid-19 stats.</p>
        """
    else:
        return 'Something is broken.'

# FetchData From Mysql Database Route 
@app.route('/dbdata', methods=['GET'])
def dbdata():
    data=[]
    allUS_data = CovidStatsUs.query.all()
    for dat in allUS_data:
        data.append(dat.state+" "+dat.case+" "+dat.death+" "+dat.updated)

    allCountry_data = CovidStatsCountryRegion.query.all()
    for dat in allCountry_data:
        data.append(dat.country_region+" "+dat.confirmed+" "+dat.deaths+" "+dat.recovered+" "+dat.last_updated)

    allCountryStats_data = CovidStatsCountry.query.all()
    for dat in allCountryStats_data:
        data.append(dat.countrycode+" "+dat.date+" "+dat.cases+" "+dat.deaths+" "+dat.recovered)
    
    return str(data)

# FetchData From API Servers Route 
@app.route('/fetchdata', methods=['GET'])
def fetchdata():

    # Api URLs stored in am array
    URLs=["https://thevirustracker.com/timeline/map-data.json",
    "https://finnhub.io/api/v1/covid19/us",
    "https://2019ncov.asia/api/country_region"]

    # Iterate through the fetched API data and stored in mysql Databases
    def virustrackerApi(data):
        dat=data['data']
        for d in dat:
            countrycode=d['countrycode']
            date=d['date']
            cases=d['cases']
            deaths=d['deaths']
            recovered=d['recovered']
            new_data=CovidStatsCountry(countrycode,date,cases,deaths,recovered)
            db.session.add(new_data)
            db.session.commit()

        print("Data of First API Stored in DB")

    # Iterate through the fetched API data and stored in mysql Databases
    def finnhubApi(data):
        for d in data:
            state=d['state']
            case=d['case']
            death=d['death']
            updated=d['updated']
            new_data=CovidStatsUs(state,case,death,updated)
            db.session.add(new_data)
            db.session.commit()

        print("Data of Second API Stored in DB")
    
    # Iterate through the fetched API data and stored in mysql Databases
    def covidAsiaApi(data):
        dat=data['results']
        for d in dat:
            country_region=d['country_region']
            confirmed=d['confirmed']
            deaths=d['deaths']
            recovered=d['recovered']
            last_updated=d['last_updated']
            new_data=CovidStatsCountryRegion(country_region,confirmed,deaths,recovered,last_updated)
            db.session.add(new_data)
            db.session.commit()

        print("Data of Third API Stored in DB")

    count=0
    # Iterate through API URLs to fetch data one by one
    for url in URLs:
        r = requests.get(url = url) 
        # extracting data in json format 
        data = r.json()
        if count==0:
            virustrackerApi(data)
        if count==1:
            finnhubApi(data)
        if count==2:
            covidAsiaApi(data)

        count=count+1

    return """
            <h1>Fetched data from 3 online covid-19 API Servers</h1>
            <p>And stored in local Database(phpmyadmin_Mysql) using Xampp Server.</p>
        """