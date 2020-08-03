#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# importing libraries
from datetime import datetime
from datetime import timedelta
from urllib.request import urlopen as UReq
from bs4 import BeautifulSoup as soup
now = datetime.now()
todaysDay = now.day
todaysMonth = now.month

#Fetching altomfotball webpage
my_url = "http://www.altomfotball.no/element.do?cmd=tournament&tournamentId=1&useFullUrl=false"
uClient = UReq(my_url)
oversiktsside = uClient.read()
uClient.close()

#Tables for upcoming matches
datoliste = []
rundeliste = []
konkurranseliste = []
hjemmelagliste = []
stillingliste = []
bortelagliste = []
kanalliste = []

#HTML parsing
page_soup = soup(oversiktsside, "html.parser")

#fills the individual lists with information about the upcoming round
for nestekamper in page_soup.find('table', id='sd_fixtures_table_next').tbody.findAll('tr'):

    dato = nestekamper.find('td', class_='sd_fixtures_date').text.strip()
    if dato == "":
        datoliste.append(datoliste[-1])
    else:
        datoliste.append(dato)
    
    runde = nestekamper.find('td', class_="sd_fixtures_round").text.strip()
    rundeliste.append(runde)
    
    konkurranse = nestekamper.find('td', class_='sd_fixtures_tournament').text.strip()
    konkurranseliste.append(konkurranse)
    
    hjemmelag = nestekamper.find('td', class_='sd_fixtures_home').text.strip()
    hjemmelagliste.append(hjemmelag)
    
    tidspunkt = nestekamper.find('td', class_='sd_fixtures_score').text.strip()
    stillingliste.append(tidspunkt)
    
    bortelag = nestekamper.find('td', class_='sd_fixtures_away').text.strip()
    bortelagliste.append(bortelag)
    
    kanal = nestekamper.find('td', class_='sd_fixtures_sumo').text.strip()
    kanalliste.append(kanal)

#Creates a string formatted in such a way that reddit will interpret it as a meaningful table
def oppkommendeKamper():
    newline = "#Denne rundens kamper: \n"  
    kommendekamperstreng = "Dato|Runde|Hjemmelag|Tidspunkt|Bortelag|Kanal" + "\n"
    allignment = ":---------:|:---------:|:---------:|:---------:|:---------:|:---------:" + "\n"
    newline += kommendekamperstreng + allignment
    
    for i in range(len(datoliste)):
        newline += datoliste[i] + "|" 
        newline += rundeliste[i] + "|"
        newline +=  hjemmelagliste[i] + "|"
        newline += stillingliste[i] + "|"
        newline += bortelagliste[i] + "|"
        newline += kanalliste[i]
        newline += "\n"
    return newline

#Tables for league table
plasser = []
lagnavn = []
kamper = []
vunnet = []
uavgjort = []
tap = []
scorede = []
innsluppne = []
forskjell = []
poeng = []

#Fills the individual league table lists with information
for tabellen in page_soup.find('table', id='sd_table_1').tbody.findAll('tr'):
    plasseringen = tabellen.findNext('td')
    navnet = plasseringen.findNext('td')
    kampene = navnet.findNext('td')
    seire = kampene.findNext('td')
    uavgjorte = seire.findNext('td')
    tapene = uavgjorte.findNext('td')
    goalsscored = tapene.findNext('td')
    goalsconceded = goalsscored.findNext('td')
    goald = goalsconceded.findNext('td')
    poengene = goald.findNext('td')
    
    plasser.append(plasseringen.text.strip())
    lagnavn.append(navnet.text.strip())
    kamper.append(kampene.text.strip())
    vunnet.append(seire.text.strip())
    uavgjort.append(uavgjorte.text.strip())
    tap.append(tapene.text.strip())
    scorede.append(goalsscored.text.strip())
    innsluppne.append(goalsconceded.text.strip())
    forskjell.append(goald.text.strip())
    poeng.append(poengene.text.strip())

#Creates a single string formatted in such a way that it creates a meaningful table on reddit
def tabellen():
    newline = "#Tabellen før runden: \n \n"
    colors = "######[](http://reddit.com#)" + "\n"
    headers = "Plass|Lagnavn|K|S|U|T|+|-|+/-|Poeng" + "\n"
    allignment = ":---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:" + "\n"
    newline += colors + headers + allignment
    
    for i in range(len(plasser)):
        newline += plasser[i] + "|"
        newline += lagnavn[i] + "|" 
        newline += kamper[i] + "|"
        newline += vunnet[i] + "|"
        newline += uavgjort[i] + "|"
        newline += tap[i] + "|"
        newline += scorede[i] + "|"
        newline += innsluppne[i] + "|"
        newline += forskjell[i] + "|"
        newline += poeng[i]
        newline += "\n"
    return newline

#Creates a string of 
def createGameweekThread():
    output = ""
    output += tabellen() + "\n" + oppkommendeKamper()
    return output

#Checks if it is fewer than 24 hours till the next match
def shouldCreateThread():
    create = False
    nextMatch = datoliste[0].replace(".", " ")
    datenextmatch = datetime.strptime(nextMatch, '%d %m %Y')
    difference = datenextmatch - now
    hourstillnextmatch = difference / timedelta(hours=1)
    if hourstillnextmatch < 24:
        create = True
    return create

def getGameRound():
    return rundeliste[0]

print(createGameweekThread())
