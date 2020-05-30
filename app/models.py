from app import db


# Flask Model for all the countries Covid19 stats from the very first reported case
class CovidStatsCountry(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    country = db.Column(db.String(15)) 
    tests = db.Column(db.String(10)) 
    cases = db.Column(db.String(10)) 
    deaths = db.Column(db.String(10)) 
    recovered = db.Column(db.String(10)) 

    def __init__(self,country,tests,cases,deaths,recovered):
        self.country=country
        self.tests=tests
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