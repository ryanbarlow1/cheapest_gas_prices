import requests
import pandas

import datetime_translator

brandIds = { 202, 88, 31, 123, 101, 122, 36, 48, 135 }
data = {}

for brandId in brandIds:
    headers = { 'User-Agent': '', 'content-type': 'application/json' }
    jsonData = '{"variables":{"area":"salt-lake","brandId":%d,"countryCode":"US","criteria":{"location_type":"county"},"fuel":1,"maxAge":0,"regionCode":"UT"},"query":"query LocationByArea($area: String, $brandId: Int, $countryCode: String, $criteria: Criteria, $fuel: Int, $maxAge: Int, $regionCode: String) { locationByArea( area: $area countryCode: $countryCode criteria: $criteria regionCode: $regionCode ) { displayName locationType stations(brandId: $brandId, fuel: $fuel, maxAge: $maxAge) { results { address { country line1 line2 locality postalCode region  } brands { brandId name } latitude longitude id name prices(fuel: $fuel) { credit { nickname postedTime price  } fuelProduct } } } } }"}' %(brandId)
    #jsonData = '{"variables":{"area":"davis","brandId":%d,"countryCode":"US","criteria":{"location_type":"county"},"fuel":1,"maxAge":0,"regionCode":"UT"},"query":"query LocationByArea($area: String, $brandId: Int, $countryCode: String, $criteria: Criteria, $fuel: Int, $maxAge: Int, $regionCode: String) { locationByArea( area: $area countryCode: $countryCode criteria: $criteria regionCode: $regionCode ) { displayName locationType stations(brandId: $brandId, fuel: $fuel, maxAge: $maxAge) { results { address { country line1 line2 locality postalCode region  } brands { brandId name } latitude longitude id name prices(fuel: $fuel) { credit { nickname postedTime price  } fuelProduct } } } } }"}' %(brandId)
    response = requests.post('https://www.gasbuddy.com/graphql', headers=headers, data=jsonData)
    jsonResponse = response.json()
    stations = jsonResponse['data']['locationByArea']['stations']

    for station in stations['results']:
        if station['prices'][0]['credit']['price'] != 0:
            stationId = station['id']
            data[stationId] = {
                'StationName': station['name'],
                'BrandName': station['brands'][0]['name'],
                'AddressLine1': station['address']['line1'],
                'City': station['address']['locality'],
                'RegularFuelPrice': '${:.2f}'.format(station['prices'][0]['credit']['price']),
                'TimeSinceReported': datetime_translator.translate(station['prices'][0]['credit']['postedTime']),
                'ReportedBy': station['prices'][0]['credit']['nickname']
            }

output = pandas.DataFrame(data)
output.transpose().sort_values(by='RegularFuelPrice')

print(output)