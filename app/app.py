from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.secret_key = 'shhhh...iAmASecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/covid19'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

print(db)

# Flask Model for all the countries Covid19 stats from the very first reported case
class CovidStatsCountry(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    countrycode = db.Column(db.String(15)) 
    date = db.Column(db.String(10)) 
    cases = db.Column(db.String(10)) 
    deaths = db.Column(db.String(10)) 
    recovered = db.Column(db.String(10)) 

    def __init__(self,countrycode,date,cases,deaths,recovered):
        self.countrycode=countrycode
        self.date=date
        self.cases=cases
        self.deaths=deaths
        self.recovered=recovered

# Flask Model for the Covid19 stats of the states of the US
class CovidStatsUs(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    state = db.Column(db.String(15)) 
    case = db.Column(db.String(10)) 
    death = db.Column(db.String(10)) 
    updated = db.Column(db.String(10)) 

    def __init__(self,state,case,death,updated):
        self.state=state
        self.case=case
        self.death=death
        self.updated=updated

# Flask Model for the Covid19 stats of overall cases results up to date for all the countries 
class CovidStatsCountryRegion(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    country_region = db.Column(db.String(15)) 
    confirmed = db.Column(db.String(10)) 
    deaths = db.Column(db.String(10)) 
    recovered = db.Column(db.String(10)) 
    last_updated = db.Column(db.String(10)) 

    def __init__(self,country_region,confirmed,deaths,recovered,last_updated):
        self.country_region=country_region
        self.confirmed=confirmed
        self.deaths=deaths
        self.recovered=recovered
        self.last_updated=last_updated

db.create_all()

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

# FetchData Route 
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

if __name__ == '__main__':
    app.run(debug=True)