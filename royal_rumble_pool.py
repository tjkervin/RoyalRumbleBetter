import csv
import random
import string
import argparse

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process for reporting on Cloud Server Secuirty Status in JUnit form for Jenkins.')
   parser.add_argument('-b', '--betters', required=True, action='store',
                       help='Provide a list of people Betting.')
   parser.add_argument('-c', '--competitors', required=False, action='store',
                       help='The Number of Competitors.', default="30")
   parser.add_argument('-r', '--rumbles', required=False, action='store',
                       help='Number of Royal Rumbles to Generate', default="2")
   args = parser.parse_args()
   return args

def convertCSVToDictList(fileName):
    headers = []
    csvDataDict = []
    with open(fileName) as csvFile:
        spamreader = csv.reader(csvFile)
        line_count = 0
        for row in spamreader:
            if line_count == 0:
                header_count = 0
                for element in row:
                    headers.insert(header_count, element) 
                    header_count += 1
                line_count += 1
            else: 
                currentItem = {}
                item_number = 0
                for element in row:
                    currentItem[headers[item_number]] = element
                    item_number += 1
                csvDataDict.append(currentItem)
    return csvDataDict

def pickFairBetterIndexWithExcess(betters, excessBettersList):
    if (len(betters) >= len(excessBettersList)) or (len(excessBettersList) == 0):
        return betters.index(random.choice(betters))
    returnBetterIndex = -1
    while (returnBetterIndex < 0):
        randomBetter = random.choice(betters)
        if randomBetter not in excessBettersList:
            returnBetterIndex = betters.index(randomBetter)

    return returnBetterIndex

def getLoadedBettersList (betters, numberOfCompetitors, excessBettersList):
    loadedBettersList = []
    numberOfEntriesEach = numberOfCompetitors / len(betters)
    numberOfEntriesLeftover = numberOfCompetitors % len(betters)
    for better in betters:
        loadedBetters = {'name': better, 'entries': numberOfEntriesEach}
        loadedBettersList.append(loadedBetters)
    
    while (numberOfEntriesLeftover > 0):
        indexOfBetter = pickFairBetterIndexWithExcess(betters, excessBettersList)
        loadedBettersList[indexOfBetter]['entries'] += 1
        excessBettersList.append(loadedBettersList[indexOfBetter]['name'])
        numberOfEntriesLeftover -= 1
    
    return {'loadedBettersList': loadedBettersList, 'excessBettersList': excessBettersList}

def generateRoyalRumbleList(loadedBettersList, numberOfCompetitors):
    rumbleList = []
    currentCompetitorNumber = 0
    while (currentCompetitorNumber < numberOfCompetitors):
        better = random.choice(loadedBettersList)
        while (better['entries'] == 0):
            better = random.choice(loadedBettersList)
        rrEntry = {'Entry': len(rumbleList) + 1, 'Name': better['name'], 'Superstar': ''}
        rumbleList.append(rrEntry)
        better['entries'] -= 1
        currentCompetitorNumber += 1
    return rumbleList
def generateRumbleCSV(rumbleList, rumbleNumber):
    rrOutputFile = "royalRumbe" + str(rumbleNumber) + ".csv"
    print ("Generating Royal Rumble Number " + str(rumbleNumber) + " to " + rrOutputFile)
    count = 0
    output_file = open(rrOutputFile, 'w')
    csvwriter = csv.writer(output_file)
    for rumble in rumbleList:
        if count == 0:
            header = rumble.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(rumble.values())
    output_file.close()
    print ("Generated Rumble Complete")
   
def generateRoyalRumble(loadedBettersList, numberOfCompetitors, rumbleNumber):
    rumbleList = generateRoyalRumbleList(loadedBettersList, numberOfCompetitors)
    generateRumbleCSV(rumbleList,rumbleNumber)
    
args = GetArgs()
numberOfRumbles = int(args.rumbles)
numberOfCompetitors = int(args.competitors)
betters = args.betters.split(",")
excessBettersList = []
rumbleCount = 0
while(rumbleCount < numberOfRumbles):
    loadedBetters = getLoadedBettersList(betters, numberOfCompetitors, excessBettersList)
    loadedBettersList = loadedBetters['loadedBettersList']
    excessBettersList = loadedBetters['excessBettersList']
    generateRoyalRumble(loadedBettersList, numberOfCompetitors,rumbleCount)
    rumbleCount += 1
