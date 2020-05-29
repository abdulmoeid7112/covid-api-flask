from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'shhhh...iAmASecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/covid19'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

print(db)

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

@app.route('/', methods=['GET'])
def index():
    if (db):
        return 'It works.'
    else:
        return 'Something is broken.'

@app.route('/fetchdata', methods=['GET'])
def fetchdata():
    return "Fecthing Data"
if __name__ == '__main__':
    app.run(debug=True)