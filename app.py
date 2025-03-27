from flask import Flask, render_template, request, send_file
import requests
import time
import csv

app = Flask(__name__)

API_KEY = 'd92705cdda54ea6a789e52d947c527b3'

# List of cities in India to track
cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad']

def get_weather_data(city, units):
    unit_symbol = "°C" if units == "metric" else "K"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        avg_temp = (data['main']['temp_max'] + data['main']['temp_min']) / 2
        weather_info = {
            'city': data['name'],
            'temperature': f"{data['main']['temp']} {unit_symbol}",
            'feels_like': f"{data['main']['feels_like']} {unit_symbol}",
            'description': data['weather'][0]['description'],
            'main': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(data['dt'])),
            'temp_max': f"{data['main']['temp_max']} {unit_symbol}",
            'temp_min': f"{data['main']['temp_min']} {unit_symbol}",
            'avg_temp': f"{avg_temp} {unit_symbol}",
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather_info
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    units = request.form.get('units', 'metric')  # Default to Celsius (metric)
    weather_data = [get_weather_data(city, units) for city in cities]
    return render_template('index.html', weather_data=weather_data, units=units)

@app.route('/download_report')
def download_report():
    units = request.args.get('units', 'metric')  # Use units from query params
    weather_data = [get_weather_data(city, units) for city in cities]
    report_file = 'weather_report.csv'

    # Writing data to CSV
    with open(report_file, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['City', 'Temperature', 'Feels Like', 'Max Temp', 'Min Temp', 
                         'Average Temp', 'Humidity (%)', 'Wind Speed (m/s)', 'Main', 'Description', 'Time'])

        for weather in weather_data:
            writer.writerow([weather['city'], weather['temperature'], weather['feels_like'], weather['temp_max'],
                             weather['temp_min'], weather['avg_temp'], weather['humidity'], weather['wind_speed'],
                             weather['main'], weather['description'], weather['time']])
    
    return send_file(report_file, as_attachment=True, download_name='weather_report.csv')

if __name__ == '__main__':
    app.run(debug=True)
