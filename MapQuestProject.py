#key = TU49GxMLfRvN6mw1eiSuAVZ8sG6lzHmA
import urllib.parse
import urllib.request
import json

class MapQuest:
    def __init__(self, APIkey):
        self._BASE_URL1 = "http://open.mapquestapi.com/directions/v2/route?"
        self._BASE_URL2 = "http://www.mapquestapi.com/geocoding/v1/address"
        self._BASE_URL3 = "http://www.mapquestapi.com/search/v4/place"
        self._API = APIkey
        self._locationList = []
        
    def helper(self, locationList):
        routeDetails = {'key': self._API, 'from': locationList[0], 'to': locationList[1:]}
        formattedDetails = urllib.parse.urlencode(routeDetails, True)
        
        requestURL = self._BASE_URL1 + formattedDetails
        
        return requestURL
        
    def totalDistance(self, locationList):
        response = None
        try:
            response = urllib.request.urlopen(self.helper(locationList))
        
            return (json.load(response)['route']['distance'])
        finally:
            if response != None:
                response.close()
        
    def totalTime(self, locationList):
        response = None
        try:
            response = urllib.request.urlopen(self.helper(locationList))
        
            return json.load(response)['route']['time']
        finally:
            if response != None:
                response.close()
        
    def directions(self, locationList):
        response = None
        try:
            response = urllib.request.urlopen(self.helper(locationList))
            finalAnswer = ''
            for j in (json.load(response)['route']['legs']):
                for i in j['maneuvers']:
                    finalAnswer += (i['narrative']) + '\n'
                
            return finalAnswer
        finally:
            if response != None:
                response.close()
    def pointOfInterest(self, locations, keyword, results):
        searchResponse = None
        geocodeResponse = None
        resultList = []
        try:
            geocodeDetails = {'key': self._API, 'location': locations}
            geocodeURL = self._BASE_URL2 + '?' + urllib.parse.urlencode(geocodeDetails, True)
            geocodeResponse = urllib.request.urlopen(geocodeURL)
            coordResult = json.load(geocodeResponse)['results'][0]['locations'][0]['latLng']
            coordinates = str(coordResult['lng']) + ',' + str(coordResult['lat'])
            
            searchDetails = {'location': coordinates, "sort": 'distance', 'feedback': 'false', 'key': self._API, 'q': keyword, 'pageSize': results}
            searchURL = self._BASE_URL3 + '?' + urllib.parse.urlencode(searchDetails, True)
            searchResponse = urllib.request.urlopen(searchURL)
            for searchResult in json.load(searchResponse)['results']:
                resultList.append(searchResult['displayString'])
            
            return resultList
        finally:
            if geocodeResponse != None:
                geocodeResponse.close()
            if searchResponse != None:
                searchResponse.close()
        

# m = MapQuest('TU49GxMLfRvN6mw1eiSuAVZ8sG6lzHmA')
# locations = ['3750 barranca pkwy, Irvine, CA 92606', '4143 Campus Dr, Irvine, CA 92612', '3333 Bristol St, Costa Mesa, CA']
# #m.totalDistance(locations)
# m.pointOfInterest(locations)
