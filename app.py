import requests, sys, json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] =  True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), nullable = False)


@app.route('/', methods = ['GET','POST'])
def index():
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
	appid = 'fa4724f5f22671dd87b730a82c8a3e5a'
	weather_list = []
	
	if request.method == 'POST':
		new_city = request.form.get('city').lower()
		#prevent dubplicate city by deleting old ones and add new one to db
		existed = []
		existed = City.query.filter_by(name=new_city)
		for each in existed:
			db.session.delete(each)
			db.session.commit()

		new_city_obj = City(name=new_city)
		db.session.add(new_city_obj)
		db.session.commit()

	cities = City.query.all()
	for city in cities:
		res = requests.get(url.format(city.name, appid)).json()
		if res['cod'] != '404':
			weather_obj = {
			'icon' : res['weather'][0]['icon'],
			'description' : res['weather'][0]['description'],
			'temp' : res['main']['temp'],
			'city_name' : res['name'],
			}
			weather_list.insert(0, weather_obj)
		
	return render_template('weather.html', weather_list = weather_list)

if __name__ == '__main__':
    app.run(DEBUG=True)
