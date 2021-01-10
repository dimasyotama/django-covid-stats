from django.shortcuts import render
import requests
import json
import datetime
# Create your views here.

def each_country(request):
    response_worldwide = requests.get('https://covid19.mathdro.id/api')
    data_worldwide = response_worldwide.json()
    confirmed_worldwide = data_worldwide['confirmed']
    recovered_worldwide = data_worldwide['recovered']
    deaths_worldwide = data_worldwide['deaths']
    date_and_time = datetime.datetime.now()
    datetime_now = date_and_time.strftime('%Y-%m-%d %H:%M') 
    country_name = {}
    if 'country' in request.GET:
        country_name = request.GET['country']
        country_name = country_name.title()
        url_catch_1 = 'https://covid19.mathdro.id/api/countries'
        response_get_url = requests.get(url_catch_1)
        data_json_1 = response_get_url.json()
        countries_name = data_json_1['countries']
        for i in countries_name:
            try:
                if country_name.title() == i['name'] or country_name.upper() != i['iso2'] or country_name.upper() != i['iso3']:
                    url_catch_2 = 'https://covid19.mathdro.id/api/countries/%s' % country_name
                    response_get_url_2 = requests.get(url_catch_2)
                    data_json_2 = response_get_url_2.json()
                    confirmed = data_json_2['confirmed']
                    recovered = data_json_2['recovered']
                    deaths = data_json_2['deaths']
                    categories = list()
                    data_require = list()
                    categories.extend(["Confirmed","Recoverd","Deaths"])
                    data_require.extend([confirmed['value'],recovered['value'],deaths['value']])
                    context = {
                        'title':"Corona Statistics from %s" %(country_name),
                        'categories':categories,
                        'data':data_require,
                        'countries_name':country_name,
                        'confirmed_value_worldwide':confirmed_worldwide['value'],
                        'recovered_value_worldwide':recovered_worldwide['value'],
                        'datetime_local':datetime_now,
                        'death_value_worldwide':deaths_worldwide['value'],
                    }
                    return render(request,'results.html',context)
                
                else:
                    country_name.title()
                    return render(request,'results.html',
                    {
                        'confirmed_value_worldwide':confirmed_worldwide['value'],
                        'recovered_value_worldwide':recovered_worldwide['value'],
                        'last_update_worldwide':data_worldwide['lastUpdate'],
                        'death_value_worldwide':deaths_worldwide['value']
                        }
                    )
            except:
                return render(request,'results.html',
                    {
                        'confirmed_value_worldwide':confirmed_worldwide['value'],
                        'recovered_value_worldwide':recovered_worldwide['value'],
                        'last_update_worldwide':data_worldwide['lastUpdate'],
                        'death_value_worldwide':deaths_worldwide['value']
                        }
                    )
        
    return render(request,'corona.html',{
         'confirmed_value_worldwide':confirmed_worldwide['value'],
         'recovered_value_worldwide':recovered_worldwide['value'],
         'last_update_worldwide':data_worldwide['lastUpdate'],
         'death_value_worldwide':deaths_worldwide['value'],
         'datetime_local':datetime_now
            })