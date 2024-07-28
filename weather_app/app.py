from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

coordinates = {
    'Istanbul': (41.0151, 28.9794),
    'New York': (40.7128, -74.0060),
    'Los Angeles': (34.0522, -118.2437),
    'London': (51.5074, -0.1278),
    'Paris': (48.8566, 2.3522),
    'Tokyo': (35.6762, 139.6503),
    'Sydney': (-33.8688, 151.2093),
    'Berlin': (52.52, 13.4050),
    'Moscow': (55.7558, 37.6176),
    'Akhisar': (38.9208, 27.8608),
    'Eskişehir': (39.7767, 30.5222)
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    if city not in coordinates:
        return jsonify({'error': 'City not supported'}), 404

    latitude, longitude = coordinates[city]
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,weathercode,wind_speed_10m'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temperature = data['hourly']['temperature_2m'][0]
        precipitation = data['hourly']['precipitation'][0]
        weather_code = data['hourly']['weathercode'][0]
        wind_speed = data['hourly']['wind_speed_10m'][0]

        return jsonify({
            'city': city,
            'temperature': f'{temperature}°C',
            'precipitation': f'{precipitation} mm',
            'weather_code': weather_code,
            'wind_speed': f'{wind_speed} km/h'
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
