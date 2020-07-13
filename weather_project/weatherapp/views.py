from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests
import datetime

def index(request) :
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=58f612f7fc0f3705abca1bc65ae1f855'
    error_msg = ''
    msg = ''
    msg_class = ''
    # city = 'India'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            # existing_city_count = City.objects.filter(name = new_city).count()
            r = requests.get(url.format(new_city)).json()
            # print("Check " + str(r))
            # getting validation for invalid city
            if r['cod'] == 200:
                form.save()
            else :
                error_msg = "Invalid City"
            # else :
            #     error_msg = "City Already Exists"
        if error_msg :
            msg = error_msg
            # giving css style
            msg_class = "danger"
        else :
            # msg = "City Added Successfully"
            msg_class = "success"

    form = CityForm()

    cities = City.objects.all()
    count = cities.count()
    # print("Count is " + str(count))

    if count == 0 :
        return render(request, 'weatherapp/clear.html', {'form' : form})
    else :
        # condition for valid city
        for city in cities :
            r = requests.get(url.format(city)).json()
            # print(r)

            date_time = datetime.datetime.now().strftime('%H:%M')
            # print("Time is" + str(date_time))
            date = datetime.date.today()
            # print("Date is" + str(date))

            city_weather = {
                    'city': city.name,
                    'temprature' : r['main']['temp'],
                    'description' : r['weather'][0]['description'],
                    'icon' : r['weather'][0]['icon'],
                    'presure' : r['main']['pressure'],
                    'humidity' : r['main']['humidity'],
                    'wind_speed' : r['wind']['speed'],
                    'date' : date,
                    'date_time' : date_time
            }

    print(city_weather)

    context = {
    'city_weather' : city_weather,
    'form' : form,
    'msg' : msg,
    'msg_class' : msg_class
    }

    return render(request, 'weatherapp/index.html', context)


def clear(request):
    # if user delete the cities
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=58f612f7fc0f3705abca1bc65ae1f855'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            r = requests.get(url.format(new_city)).json()
            if r['cod'] == 200:
                form.save()

        return redirect('index')
    else :
        City.objects.all().delete()
        form = CityForm()
        context = {'form' : form }
        return render(request, 'weatherapp/clear.html', context)
