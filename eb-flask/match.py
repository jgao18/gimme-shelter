#-------------------------------------------------------------------------------
# Name:        lol
# Purpose:     Get Rekt Bitch
#
# Author:      Fuckin' Brutal
#
# Created:     For Savagery
# Copyright:   (c) Twatson 2016
# Licence:     Haha
#-------------------------------------------------------------------------------

import googlemaps.client
import copy
from datetime import datetime

def getPersonLocation(personId):
    
    #read location field form person

    return "Laclede and Grand"

def getElegibleShelters(personId):

    #person get bools
    #calculate derived bools (age, tri-moridity)
    #shelters get bools and id
    #eliminate conflicting shelters
    #return shelter ids that don't conflict with person's bools

    return [0,1,2,3]

def getShelterLocarions(shelterIds):

    #read address fields from shelter table by shelter id
    #return in same order as shelter ids came in

    return ["3701 Lindell Blvd.", "New York City, New York", "Washington, DC", "Seattle, WA"]

def convertGmapsData(result, numberOfAddresses):
    rowsArray = result['rows']

    distanceValues = [0 for x in range(numberOfAddresses)]
    distanceText = copy.deepcopy(distanceValues)

    for i in range(0, numberOfAddresses, 1):
        distanceValues[i] = rowsArray[0]['elements'][i]['distance']['value']
        distanceText[i] = rowsArray[0]['elements'][i]['distance']['text']

    return [distanceValues, distanceText]


#get personId from cookie
personId = 0;
personLocation = getPersonLocation(personId)
shelters = getElegibleShelters(personId)
shelterLocations = getShelterLocarions(shelters)
gmaps = googlemaps.Client(key='AIzaSyCfb_q7APSzGK1WSk64s_i-vc6UA-XEFEY')

result = gmaps.distance_matrix(personLocation, shelterLocations)
if (result['status'] != 'OK'):
    print("Query failed: returned status" + result['status'])
    exit()

rowsDict = result['rows'][0]
convertedData = convertGmapsData(result, len(shelters))

new = []
for i in range(0, len(shelters)):
    new.append((shelters[i], convertedData[0][i], convertedData[1][i], shelterLocations[i]))

new = sorted(new, key=lambda x: x[1])
print new

# get other relevant data about shelters and package for flask displsy (unknown)
