#Mathias Novianto
#13516021
#7 Agustus 2018
#Data scraping dari website Kuala Lumpur International Airport
#Tugas Seleksi Lab Basis Data
#Viel Gluck!

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time
import json
import os

#make soup of all flight to json
def allFlightToDictionary(all_flight, type, date):
    dictionaryList = []
    for flight in all_flight:
        flightData = flight.findAll("td")
        flightDictionary = {}
        if(type == "arrival"):
            if(len(flightData)<7):
                continue
            flightDictionary['date'] = date
            flightDictionary['from'] = flightData[0].text
            flightDictionary['to'] = flightData[1].text
            flightDictionary['code'] = flightData[3].text
            flightDictionary['status'] = flightData[4].text
            flightDictionary['sta'] = flightData[5].text
            flightDictionary['eta'] = flightData[6].text
        else:
            if(len(flightData) < 9):
                continue
            flightDictionary['date'] = date
            flightDictionary['to'] = flightData[0].text
            flightDictionary['from'] = flightData[1].text
            flightDictionary['code'] = flightData[3].text
            flightDictionary['status'] = flightData[4].text
            flightDictionary['std'] = flightData[5].text
            flightDictionary['etd'] = flightData[6].text
            flightDictionary['gate'] = flightData[7].text
            flightDictionary['checkin'] = flightData[8].text
        dictionaryList.append(flightDictionary)
    return dictionaryList

#Make JSON file in the same folder with the program
def dumpToJSONFile(jsonFile,json_file):
    output_path = '.'
    with open(os.path.join(output_path,json_file),'w') as f_out:
        json.dump(jsonFile,f_out)

#get the next day in the calendar
def nextDate(dateInput):
    #split to year, month, day
    dateSplit = dateInput.split('-')
    year = int(dateSplit[0])
    month = int(dateSplit[1])
    day = int(dateSplit[2])
    if(year % 400 == 0):
        leap_year = True
    elif(year % 100 == 0):
        leap_year = False
    elif(year % 4 == 0):
        leap_year = True
    else:
        leap_year = False
    if month in (1,3,5,7,8,10,12):
        month_length = 31
    elif(month == 2):
        if leap_year:
            month_length = 29
        else:
            month_length = 28
    else:
        month_length = 30

    if (day < month_length):
        day += 1
    else:
        day = 1
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    strYear = str(year)
    if(month < 10):
        strMonth = '0'+str(month)
    else:
        strMonth = str(month)
    if(day < 10):
        strDay =  '0'+str(day)
    else:
        strDay = str(day)
    return strYear+'-'+strMonth+'-'+strDay


#example web
#http://www.klia.com.my/index.php?m=airport&c=flight_schedule_details&date=2018-05-01&flighttype=departure&aid=1
klia_base_web_beginning = "http://www.klia.com.my/index.php?m=airport&c=flight_schedule_details&date="
klia_base_web_end = "=departure&aid=1"

#date format : yyyy-mm-dd, example : date = '2018-05-07'
print("Please enter date you want to search : (yyyy-mm-dd)")
date = input()
print("How many days ?")
numberOfDays = int(input())
#can be departure or arrival, example : flightType = 'arrival'
print("Please enter type of flight you want to search (departure/arrival) : ")
flightType = input()

#initialize 'data' type to an array
data = []

for days in range(0,numberOfDays):
    #sleep for 0,5 second, prevent suspicion from server
    time.sleep(0.5)
    klia_full_web = klia_base_web_beginning+date+"&flighttype="+flightType+klia_base_web_end
    open_klia_web = uReq(klia_full_web)
    raw_html = open_klia_web.read()
    klia_soup = soup(raw_html,'html.parser')

    #arrival and departure in the same page, but different id tag
    if(flightType=='arrival'):
        div = klia_soup.find(id="arrival-flight")
    else:
        div = klia_soup.find(id="departure-flight")
    all_flight = div.findAll("tr")

    data = data + allFlightToDictionary(all_flight[1:],flightType,date)

    #Get the next day for next iteration
    if(days<numberOfDays-1):
        date = nextDate(date)

dumpToJSONFile(data, date + "-" + flightType+'-'+str(numberOfDays)+".json")
print("Process done ! Please check the json file")
