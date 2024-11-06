import requests
from django.shortcuts import render
from .forms import CityForm

def get_weather(request):
    api_key = "79dbd950cc8c4d2da2194924243110"
    url = "http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=7&aqi=no&alerts=no"

    weather_data = []
    city_name = ""
    country_name = ""
    
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            response = requests.get(url.format(api_key, city))  

            if response.status_code == 200:
                try:
                    data = response.json()

                    # Зберігаємо інформацію про місто та країну
                    city_name = data["location"]["name"]
                    country_name = data["location"]["country"]

                    # Отримуємо прогноз для кожного дня
                    for day in data["forecast"]["forecastday"]:
                        date = day["date"]
                        temperature = day["day"]["avgtemp_c"]
                        condition = day["day"]["condition"]["text"].lower()
                        icon = day["day"]["condition"]["icon"]

                        # Встановлюємо рекомендацію залежно від погоди
                        if "sunny" in condition or temperature >= 20:
                            recommendation = "The weather is great for a walk in the fresh air! Consider wearing sunglasses and a hat."
                        elif "rain" in condition or temperature < 10:
                            recommendation = "It is better to stay at home, drink tea or read a book. If you go outside, wear a raincoat and take an umbrella."
                        elif "cloudy" in condition:
                            recommendation = "A light jacket would be a good idea. It's a bit chilly, but still nice for a stroll."
                        elif "snow" in condition:
                            recommendation = "Make sure to bundle up! Wear warm clothing, a coat, and a scarf."
                        else:
                            recommendation = "The weather is mild. Dress comfortably."

                        # Додаємо інформацію для кожного дня в список weather_data
                        weather_data.append({
                            'city': city_name,
                            'country': country_name,
                            'date': date,
                            'temperature': temperature,
                            'condition': condition,
                            'icon': icon,
                            'recommendation': recommendation  # Додаємо рекомендацію для кожного дня
                        })

                except ValueError:
                    print("Error: Answer is not valid JSON")
            else:
                print(f"Error: Server response failed - {response.status_code}")

    else:
        form = CityForm()

    return render(request, 'weather/weather.html', {
        'form': form,
        'weather_data': weather_data,
        'city_name': city_name,
        'country_name': country_name
    })
