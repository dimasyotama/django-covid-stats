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
        # print(country_name)
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
                    print(confirmed)
                    # list_of_categories = ["Case Confirmed","Case Recovered","Deaths Case"]
                    # categories = list()
                    # for i in list_of_categories:
                    #     categories.append(i)
                    confirmed_case = {
                        'name':list_of_categories[0],
                        'data': [confirmed['value']],
                        'color':'#ffe37d'
                    }
                    recovered_case = {
                        'name':list_of_categories[1],
                        'data':[recovered['value']],
                        'color': '#9cff6e'
                    }
                    deaths_case = {
                        'name': list_of_categories[2],
                        'data':[deaths['value']],
                        'color' : '#ff5640'
                    }
                    country = country_name
                    chart = {
                        'chart':{'type':'column'},
                        'title':{'text':'COVID-19 Stats in %s'%(country_name)},
                        # 'xAxis':{'categories':'%s'%()},
                        'series':[confirmed_case,recovered_case,deaths_case]
                    }
                    dump_the_data = json.dumps(chart)
                    context = {
                        'navs':'graphics',
                        'chart':dump_the_data,
                        'confirmed_value_worldwide':confirmed_worldwide['value'],
                        'recovered_value_worldwide':recovered_worldwide['value'],
                        'datetime_local':datetime_now,
                        'death_value_worldwide':deaths_worldwide['value'],
                    }
                    print(dump_the_data)
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