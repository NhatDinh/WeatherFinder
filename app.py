import requests, sys, json, sqlite3
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
	weather_list = []

	if request.method == 'POST':
		new_city = request.form.get('city').lower()
		if new_city:
			dup = City.query.filter_by(name=new_city).first()
			if not dup:
				new_city_entry = City(name=new_city)
				db.session.add(new_city_entry)
				db.session.commit()
	
	cities = City.query.all()
	for city in cities:
		weather_obj = get_weather_obj(city.name)
		weather_list.insert(0, weather_obj)

	conn = sqlite3.connect('weather.db')
	c = conn.cursor()

	city_arr = []
	for city in c.execute('SELECT * FROM City'):
		city_arr.append(city)
		print(city)
        

	return render_template('weather.html', weather_list = weather_list, city_arr = city_arr)
 
def get_weather_obj(name):
	url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
	appid = 'fa4724f5f22671dd87b730a82c8a3e5a'
	res = requests.get(url.format(name, appid)).json()
	weather_obj = {}
	if res['cod'] != '404':
			weather_obj = {
			'icon' : res['weather'][0]['icon'],
			'description' : res['weather'][0]['description'],
			'temp' : res['main']['temp'],
			'city_name' : res['name'],
			}
	return weather_obj


if __name__ == '__main__':
    app.run(debug=True)
