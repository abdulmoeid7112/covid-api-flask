from flask import make_response
from flask import current_app as app
from models import db, CovidStatsCountry, CovidStatsCountryRegion, CovidStatsUs
from flask_restful import Resource, Api
from flask import jsonify
import requests

api = Api(app)

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

# FetchData From Mysql Database Route Starts Here
class USStatesData(Resource):
    def get(self):
        records = [dict({
            "id": dat.id,
            "state": dat.state,
            "case": dat.case,
            "death": dat.death,
            "updated": dat.updated,
        }) for dat in CovidStatsUs.query.all()]

        return jsonify(records)

class USState(Resource):
    def get(self, id):
        dat = CovidStatsUs.query.get(int(id))
        if dat:
            record = {
                "id": dat.id,
                "state": dat.state,
                "case": dat.case,
                "death": dat.death,
                "updated": dat.updated,
            }
            return jsonify(record)
        else:
            record = {
                "message": "Result Not Found"
            }
            return jsonify(record), 404

api.add_resource(USStatesData, '/us-states')
api.add_resource(USState, '/us-states/<id>')

class allCountryData(Resource):
    def get(self):
        records = [dict({
            "id": dat.id,
            "country_region": dat.country_region,
            "confirmed": dat.confirmed,
            "deaths": dat.deaths,
            "recovered": dat.recovered,
            "last_updated" : dat.last_updated
        }) for dat in CovidStatsCountryRegion.query.all()]

        return jsonify(records)

class CountryData(Resource):
    def get(self, name):
        dat = CovidStatsCountryRegion.query.filter_by(country_region=name).first()
        if dat:
            record = {
                "id": dat.id,
                "country_region": dat.country_region,
                "confirmed": dat.confirmed,
                "deaths": dat.deaths,
                "recovered": dat.recovered,
                "last_updated" : dat.last_updated
            }
            return jsonify(record)
        else:
            record = {
                "message": "Result Not Found"
            }
            return jsonify(record), 404

api.add_resource(allCountryData, '/all-country')
api.add_resource(CountryData, '/all-country/<name>')

class allCountryStats(Resource):
    def get(self):
        records = [dict({
            "id": dat.id,
            "country": dat.country,
            "tests": dat.tests,
            "cases": dat.cases,
            "deaths": dat.deaths,
            "recovered" : dat.recovered
        }) for dat in CovidStatsCountry.query.all()]

        return jsonify(records)

api.add_resource(allCountryStats, '/all-country-stats')
# ENDS Here


# FetchData From API Servers Route Start Here
class FetchAPIData(Resource):
    def post(self):
        # Api URLs stored in am array
        URLs=["https://corona.lmao.ninja/v2/countries",
        "https://finnhub.io/api/v1/covid19/us",
        "https://2019ncov.asia/api/country_region"]

        # Iterate through the fetched API data and stored in mysql Databases
        def novalCovidApi(data):
            for d in data:
                country=d['country']
                tests=d['tests']
                cases=d['cases']
                deaths=d['deaths']
                recovered=d['recovered']
                new_data=CovidStatsCountry(country,tests,cases,deaths,recovered)
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

        # Iterate through API URLs to fetch data one by one
        for count,url in enumerate(URLs):
            r = requests.get(url = url) 
            # extracting data in json format 
            data = r.json()
            if count==0:
                novalCovidApi(data)
            if count==1:
                finnhubApi(data)
            if count==2:
                covidAsiaApi(data)

        return """
                <h1>Fetched data from 3 online covid-19 API Servers</h1>
            """
api.add_resource(FetchAPIData, '/fetch-api-data')
# ENDS Here