import json
import os
import requests
import datetime
import dotenv

dotenv.load_dotenv()

current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

apiKey = os.getenv('API_KEY')

if len(apiKey) == 32:
    print('Apikey detected')

def storeFile(data, fileName):
    print(f'Storing {fileName}.')
    with open(fileName, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=1)
    print('Storing file finished.')

def getWeatherApi(writeToFile, city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    parameters = {
        'q': city,
        'AppId': apiKey,
        'units': 'metric'
    }
    response = requests.get(base_url, parameters)
    print(f'Response: {response}')
    if response.status_code == 200:
        print('Request successful!')
        jsonData = response.json()
        
    elif response.status_code == 404:
        print('404: Page not found >_<')
        return
    
    else:
        print(response.status_code)
        return      
    
    if writeToFile == 1:
        storeFile(jsonData, 'weatherData.json')

def loadJson(name):
    with open(name, 'r') as f:
        return json.load(f)

def main():
    if os.path.exists(os.path.join(current_directory, 'weatherData.json')):
        print('Data found!')
    else:
        print('No existing Data found')
    
    if input('Do you want to update with API?\n1: yes\n2: idc\n') == '1':
        city = input('Enter your city name:\n')
        getWeatherApi(1, city)
    
    jsonData = loadJson('weatherData.json')
    option = 0
    exiting = 0
    while True:
        timeZoneInSec = int(jsonData['timezone'])
        option = input('\nWhat do you want?\n1: Weather Description\n2: Your Position\n3: Temperature\n4: Cloud Stats\n5: Sun info\n10: Exit\n')
        if exiting == 1:
            break
        match int(option):
            case 1:
                print('You chose option 1. ^_____^')
                visibility = jsonData['visibility']
                #print(f'DEV SHIT: {visibility}')
                if visibility < 10000:
                    print(f"Description: {jsonData['weather'][0]['description']}\nVisibility: {jsonData['visibility']}m")
                elif visibility >= 10000:
                    print(f"Description: {jsonData['weather'][0]['description']}\nVisibility: Clear View")
            case 2:
                print('You chose option 2. ^_____^')
                print(f"Longitude: {jsonData['coord']['lon']}\nLatitude: {jsonData['coord']['lat']}\nCountry code: {jsonData['sys']['country']}\nCityname: {jsonData['name']}\nTimezone: {round(jsonData['timezone']/3600)}")
            case 3:
                print('You chose option 3. ^_____^')
                print(f'Temperature data:\nReal Temperature: {jsonData["main"]["temp"]}\nFeels like Temperature: {jsonData["main"]["feels_like"]}\nRange:\n     Min: {jsonData["main"]["temp_min"]}\n     Max: {jsonData["main"]["temp_max"]}')
            case 4:
                print('You chose option 4. ^_____^')
                print(f'Cloudines: {jsonData["visibility"]}%')
            case 5:
                sunriseTimestamp = int(jsonData["sys"]["sunrise"])
                sunsetTimestamp = int(jsonData["sys"]["sunset"])

                sunrise = datetime.fromtimestamp(sunriseTimestamp, datetime.timezone.utc) + datetime.timedelta(seconds=timeZoneInSec)
                sunset = datetime.fromtimestamp(sunsetTimestamp, datetime.timezone.utc) + datetime.timedelta(seconds=timeZoneInSec)

                print('You chose option 5. ^_____^')
                print(f'Sunrise: {sunrise.strftime("%H:%M:%S")}\nSunset: {sunset.strftime("%H:%M:%S")}')
            case 10:
                print('Exiting')
                exiting = 1
                break
            case _: 
                print('Invalid option. ¬_¬')
        input('\nPress Enter to continue...\n')


if __name__ == "__main__":

    
    main()
