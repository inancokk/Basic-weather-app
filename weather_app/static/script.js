document.getElementById('get-weather-btn').addEventListener('click', function() {
    const city = document.getElementById('city-input').value.trim();
    
    if (!city) {
        document.getElementById('weather-result').innerHTML = '<p>Please enter a city name.</p>';
        return;
    }
    
    // APIden hava durumu verisini al
    fetch(`/weather?city=${encodeURIComponent(city)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {

            const weatherResult = document.getElementById('weather-result');
            if (data.city) {
                weatherResult.innerHTML = `
                    <h2>${data.city}</h2>
                    <p>Temperature: ${data.temperature}</p>
                    <p>Precipitation: ${data.precipitation}</p>
                    <p>Weather Code: ${data.weather_code}</p>
                    <p>Wind Speed: ${data.wind_speed}</p>
                `;
            } else if (data.error) {
                weatherResult.innerHTML = `<p>${data.error}</p>`;
            } else {
                weatherResult.innerHTML = '<p>City not found</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('weather-result').innerHTML = '<p>An error occurred while fetching weather data.</p>';
        });
});
