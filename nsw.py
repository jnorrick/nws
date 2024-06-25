import os
import requests
import json

#websites for reference for when making readme:https://www.weather.gov/documentation/services-web-ap; https://open-meteo.com/en/docs
local_zone = "MOZ063"
county_zone = "MOC189"
state_area = "MO"
coords = {"latitude": 38.5951,"longitude": -90.5462}


def get_office_information(latitude, longitude):
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    response.raise_for_status()

    return response

office_information = get_office_information(**coords).json()
forecast = requests.get(office_information['properties']['forecast']).json()

# alerts_state = requests.get(f"https://api.weather.gov/alerts/active?area=MO").json()
# alerts_forecast_zone = requests.get(f"https://api.weather.gov/alerts/active?zone=MOZ063").json()
# alert_forecast_county = requests.get(f"https://api.weather.gov/alerts/active?zone=MOC189").json()

def get_local_alerts(zone):
    response = requests.get(f"https://api.weather.gov/alerts/active?zone={zone}")
    response.raise_for_status()

    return response

def get_state_alerts(area):
    response = requests.get(f"https://api.weather.gov/alerts/active?area={area}")
    response.raise_for_status()

    return response

def display_forecast(forecast):
    detailed_forecast =  forecast['properties']['periods'][0]['detailedForecast']
    
    return detailed_forecast

def display_local_alerts(zone):
    alerts = get_local_alerts(zone).json()
    #this will work if we are not sure if 'features' exists, it will return an empty array
    if not alerts.get('features', []):
        return "No current active local alerts to display."
    else:
        for alert in alerts['features']:
            alert_headline = alert['properties']['headline']
            alert_description = alert['properties']['description']
            alert_instructions = alert['properties']['instruction']
       

        return [alert_headline, alert_description, alert_instructions]
    
def display_state_alerts(area):
    alerts = get_state_alerts(area).json()
    if not alerts.get('features', []):
        return "No current active alerts to display."
    else:
        # need to account for if more than one alert is available
        for alert in alerts['features']:
            alert_headline = alert['properties']['headline']
            alert_description = alert['properties']['description']
            alert_instructions = alert['properties']['instruction']
    
    return [alert_headline, alert_description, alert_instructions]

print('*' * 50)
print("Current Forecast:")
print(display_forecast(forecast))
print('*' * 50)
print("Current Local Alerts:")
final_local_alerts = display_local_alerts(local_zone)
for alert in final_local_alerts:
    print(alert)
print('*' * 50)
