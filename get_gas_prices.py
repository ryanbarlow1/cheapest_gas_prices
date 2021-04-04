import requests
import pandas
import datetime_translator
 
brandIds = { 202, 88, 31, 123, 101, 122, 36, 48, 135, 170 }
 
stationsUrl = 'https://www.gasbuddy.com/assets-v2/api/stations?area=salt-lake&countyId=1002&regionCode=UT&countryCode=US&fuel=1&maxAge=0'
#stationsUrl = 'https://www.gasbuddy.com/assets-v2/api/stations?area=davis&countyId=1165&regionCode=UT&countryCode=US&fuel=1&maxAge=0'
#stationsUrl = 'https://www.gasbuddy.com/assets-v2/api/stations?area=weber&countyId=881&regionCode=UT&countryCode=US&fuel=1&maxAge=0'
 
headers = { 'User-Agent': '' }
stationsResponse = requests.get(stationsUrl, headers=headers)
stations = stationsResponse.json()
 
fuelsUrl = 'https://www.gasbuddy.com/assets-v2/api/fuels?fuel=1'
 
data = {}
 
for station in stations['stations']:
    if station['brand_id'] in brandIds:
        stationId = station['id']
        fuelsUrl += '&stationIds=' + str(stationId)
        data[stationId] = {
            'StationName': station['name'],
            'BrandName': station['brand_name'],
            'AddressLine1': station['address']['line_1'],
            'City': station['address']['locality']
        }
 
fuelsResponse = requests.get(fuelsUrl, headers=headers)
fuels = fuelsResponse.json()
 
for fuel in fuels['fuels']:
    if fuel['fuelType'] == 'regular_gas':
        stationId = int(fuel['stationId'])
        for price in fuel['prices']:
            if ((price['isCash'] == False) or (len(price) == 1)) and (price['price'] != 0):
                data[stationId]['RegularFuelPrice'] = price['price']
                data[stationId]['ReportedBy'] = price['reportedBy']
                data[stationId]['DaysSinceReported'] = datetime_translator.translate(price['postedTime'])

output = pandas.DataFrame(data)
output.transpose().sort_values(by='RegularFuelPrice')