from django.shortcuts import render
import requests
import json
# Create your views here.

def each_country(request):
    response_worldwide = requests.get('https://covid19.mathdro.id/api')
    data_worldwide = response_worldwide.json()
    confirmed_worldwide = data_worldwide['confirmed']
    recovered_worldwide = data_worldwide['recovered']
    deaths_worldwide = data_worldwide['deaths']
    country_name = {}
    if 'country' in request.GET:
        country_name = request.GET['country']
        country_name = country_name.title()
        print(country_name)
        url1 = 'https://covid19.mathdro.id/api/countries'
        response1 = requests.get(url1)
        data1 = response1.json()
        countries_name = data1['countries']
        for i in countries_name:
            try:
                if country_name.title() == i['name'] or country_name.upper() != i['iso2'] or country_name.upper() != i['iso3']:
                    url2 = 'https://covid19.mathdro.id/api/countries/%s' % country_name
                    response2 = requests.get(url2)
                    data2 = response2.json()
                    confirmed = data2['confirmed']
                    recovered = data2['recovered']
                    deaths = data2['deaths']
                    confirmed_case = {
                        'name':'Case Confirmed',
                        'data': [confirmed['value']],
                        'color':'#ffe37d'
                    }
                    recovered_case = {
                        'name':'Case Recoverd',
                        'data':[recovered['value']],
                        'color': '#9cff6e'
                    }
                    deaths_case = {
                        'name': 'Deaths Case',
                        'data':[deaths['value']],
                        'color' : '#ff5640'
                    }
                    country = country_name
                    chart = {
                        'chart':{'type':'column'},
                        'title':{'text':'COVID-19 Stats in %s'%(country_name)},
                        # 'xAxis':{'categories':categories},
                        'series':[confirmed_case,recovered_case,deaths_case]
                    }
                    dump_the_data = json.dumps(chart)
                    context = {
                        'navs':'graphics',
                        'chart':dump_the_data
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
            })