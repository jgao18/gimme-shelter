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
from datetime import datetime, date

def getPersonLocation(personId):
   
    conn = mysql.connect()
    cursor = conn.cursor()
 
    cursor.execute("SELECT Location FROM Resident WHERE Id=" + str(personId) + ";")
 
    return cursor.fetchone()

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getElegibleShelters(personId):

    cursor = conn.cursor.execute("SELECT DoB, Sex, Sleep_outside, Veteran_homeless, Emergency_service, Harm, Legal, Exploitation, Money, Meaningful, Self_care, Social, Physical, Substance, Mental, Medication, Abuse FROM Resident where User = " + str(personId))
    personStats = cursor.fetchone()

    dob = personStats[0]
    sex = personStats[1]

    personStats = personStats[2:]

    if dob != None and calculate_age(dob) >= 60:
        personStats = personStats + 1
    else:
        personStats = personStats + 0

    cursor = conn.cursor.execute("SELECT Id, Takes_men, Takes_women, beds_avail, Sleep_outside, Veteran_homeless, Emergency_service, Harm, Legal, Exploitation, Money, Meaningful, Self_care, Social, Physical, Substance, Mental, Medication, Abuse, Elderly FROM Shelter")
    shelterStats = cursor.fetchone()

    elegible = []
    for shelterStat in shelterStats:
        isElegible = True
        if sex == 'M':
            if shelterStat[1] != 1:
                isElegible = False
        elif sex == 'F':
            if shelterStat[2] != 1:
                isElegible = False

        if shelterStat[3] <= 0:
            isElegible = False

        for i in range(4, len(personStats)):
            if shelterStat[i] != 2 and shelterStat[i] != None and personStats[i] != None: # 2 is don't care condition
                isElegible = isElegible and shelterStat[i] == personStats[i]
        if isElegible:
            elegible.append(shelterStat)

    return [x[0] for x in elegible]

def getShelterInfo(shelterIds):

    conn = mysql.connect()
    cursor = conn.cursor()
 
    shelterLocs = [len(shelterIds)]
    for i in shelterIds:
        cursor.execute("SELECT name, addr, beds_avail, closes_by FROM Shelter WHERE Id=" + str(shelterIds[i]) + ";")
        shelterLocs[i] = cursor.fetchone()
 
    return shelterLocs

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
shelterInfo = getShelterInfo(shelters)
gmaps = googlemaps.Client(key='AIzaSyCfb_q7APSzGK1WSk64s_i-vc6UA-XEFEY')

result = gmaps.distance_matrix(personLocation, [x[1] for x in shelterInfo])
if (result['status'] != 'OK'):
    print("Query failed: returned status" + result['status'])
    exit()

rowsDict = result['rows'][0]
convertedData = convertGmapsData(result, len(shelters))

new = []
for i in range(0, len(shelters)):
    new.append((convertedData[0][i], shelters[i], convertedData[1][i]) + shelterInfo[i])

new = sorted(new, key=lambda x: x[0])
#new = [x[1:] for x in new]
print new

# get other relevant data about shelters and package for flask displsy (unknown)
