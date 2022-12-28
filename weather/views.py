from django.shortcuts import render
from django.shortcuts import redirect
import requests
from .forms import CityForm
from .models import City
from datetime import datetime
import time


def week_weather(city, weather_week):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=40&units=metric&appid=8108add2ca9ea176ffd4e7abfbb396c7&lang=ru'
    city_weather = requests.get(url).json()
    temp = []
    for i in range(0, 39):
        temp.append(city_weather['list'][i]['main']['temp'])
        d = datetime.strptime(time.ctime(int(city_weather['list'][i]['dt'])), "%a %b %d %H:%M:%S %Y")
        if i % 8 == 0:
            weather = {
                'dt': d.strftime("%a, %d %b"),
                'day_temperature': round(max(temp)),
                'night_temperature': round(min(temp)),
                'description': city_weather['list'][i-4]['weather'][0]['description']
            }
            weather_week.append(weather)
            temp = []


def main_city(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=8108add2ca9ea176ffd4e7abfbb396c7&lang=ru'
    city_weather = requests.get(url).json()
    weather = {
        'city': city,
        'temperature': round(city_weather['main']['temp']),
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon'],
        'wind': city_weather['wind']['speed'],
        'pressure': city_weather['main']['pressure']
    }
    return weather


def cities_weather(cities, weather_data):
    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid=8108add2ca9ea176ffd4e7abfbb396c7&lang=ru'
        city_weather = requests.get(url).json()
        weather = {
            'city': city.name,
            'temperature': round(city_weather['main']['temp']),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'wind': city_weather['wind']['speed'],
            'pressure': city_weather['main']['pressure']
        }
        weather_data.append(weather)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def Main_page_view(request):
    form = CityForm()
    if City.objects.filter(ip_address=get_client_ip(request)):
        count_id = City.objects.filter(ip_address=get_client_ip(request)).latest('id')
        return redirect(f'/city/{count_id.name}')
    else:
        if request.method == 'POST':
            if "Add" in request.POST:
                form = CityForm(request.POST)
                if form.is_valid():
                    ip_save(form, request)
                    count_id = City.objects.filter(ip_address=get_client_ip(request)).latest('id')
                    return redirect(f'/city/{count_id.name}')
    context = {'form': form}
    return render(request, 'main.html', context)


def Weather_view(request, name):
    cities = City.objects.filter(ip_address=get_client_ip(request))
    form = CityForm()
    weather_data = []
    weather_week = []

    if request.method == 'POST':
        if "Add" in request.POST:
            form = CityForm(request.POST)
            if form.is_valid():
                ip_save(form, request)
                count_id = City.objects.latest('id')
                return redirect(f'/city/{count_id.name}')

    if request.method == 'GET':
        if "Delete" in request.GET:
            form = request.GET.get('Delete')
            City.objects.filter(name=form).delete()
            if request.path == f'/city/{form}':
                count_id = City.objects.filter(ip_address=get_client_ip(request)).latest('id')
                return redirect(f'/city/{count_id.name}')
            else:
                return redirect(request.path)

    week_weather(name, weather_week)
    cities_weather(cities, weather_data)
    context = {'weather_data': weather_data, 'form': form, 'main_city': main_city(name), 'weather_week': weather_week}
    return render(request, 'city.html', context)


def ip_save(form, request):
    instance = form.save(commit=False)
    instance.ip_address = get_client_ip(request)
    try:
        instance.save()
    except:
        pass



