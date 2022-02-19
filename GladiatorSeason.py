import numpy
import pandas
import mysql.connector

#Connect to mySQL database
DB = mysql.connector.connect(host=Host, user=User,passwd=PassWord, database=DataBase)
mycursor = DB.cursor()

#Create class for each fighter that contains name and value of its strength
class Fighter:
    def __init__(self, Name, Stre):
        self.Name = Name
        self.Stre = Stre

#Season Schedule, each number is the number for a team, the same position in each list will be the two teams playing  
ScheduleHome = [1,3,2,4,3,4,2,4,3,1,1,2,1,3,2,4,3,4,2,4,3,1,1,2]
ScheduleAway = [2,4,3,1,1,2,1,3,2,4,3,4,2,4,3,1,1,2,1,3,2,4,3,4]

#Creates a list of fighter objects for each team, information comes from teams table in MySqlServer
Team1 = []
Team2 = []
Team3 = []
Team4 = []
#Contains all fighter information
All = []

#Keeps track of how many times each team wins and loses
Team1Win = 0
Team1Loss = 0
Team2Win = 0
Team2Loss = 0
Team3Win = 0
Team3Loss = 0
Team4Win = 0
Team4Loss = 0

#Game keeps tracks of what number of game we are on, FightNum keeps track of number of fights per game, id is primary key id
Game = 1
FightNum = 1
id = 1

#Get information for each team and save fighter information in Fighter class and make a list of all the Fighters 
mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 1";')

for w in mycursor:
    Team1.append(Fighter(w[0], w[1]))

All.append(Team1)

mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 2";')

for x in mycursor:
    Team2.append(Fighter(x[0], x[1]))

All.append(Team2)

mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 3";')

for y in mycursor:
    Team3.append(Fighter(y[0], y[1]))

All.append(Team3)

mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 4";')

for z in mycursor:
    Team4.append(Fighter(z[0], z[1]))
All.append(Team4)   

#Will be used for saving information about each fight 
LoserName = ''
WinnerName = ''
WinnerStr = 0
LoserStr = 0
HomeTeam = 0
AwayTeam = 0

#Creates function for a fight so that fights can be run multiple times. 
#Takes the home and away teams taken from the two schedule lists, FightNum and id so that the fight number and id number can be reset and/or increased with each game 
#returns id so that can be continued in another game 
def Fight(HomeTeam, AwayTeam, FightNum, id):
    #Set home to the home team and away to the away team by using schedule information then taking that team from All, subtract one because lists start at 0 in python
    Home = All[HomeTeam - 1]
    Away = All[AwayTeam - 1]
    #When a fighter loses they get removed from list so when there are no more fighters in either home or away the game is over
    while(len(Home) != 0 and len(Away) != 0):
        #Get the strength and name of each figher 
        HomeTemp = Home[0].Stre
        AwayTemp = Away[0].Stre
        HomeName = Home[0].Name
        AwayName = Away[0].Name
        
        #Get probability that home player will win, calculated by taking (strenght of fighter)/(Strength of both fighters added together)
        Prob = (1 - (HomeTemp/(HomeTemp + AwayTemp)))
        HomeProb = Prob
        #Probability of Away fighter is just home 1- prob 
        AwayProb = 1 - Prob
        #Turn probability into nmber between one and a thousand. The function will pick and number between one and a thousand and compare it to the percantage.
        Prob = Prob * 1000
        
        #Choose random number between one and a thousand
        Number = numpy.random.randint(0, 1000)
        #If Number is greater than or equalt to Probability of winning then home fighter wins, away strength is  added to home strength, move home fighter to end of list, delete away fighter  
        if Number >= Prob:
            Home[0].Stre = HomeTemp + AwayTemp
            Home.append(Home[0])
            Home.pop(0)
            Away.pop(0)
            #Description of how the fight went, will be added to the SQL command 
            Description = '"' + HomeName + '(' + str(HomeTemp) + ') for team ' + str(HomeTeam) + ' beat ' + AwayName + '(' + str(AwayTemp) + ') for team ' + str(AwayTeam) + '"' 
            WinnerName = HomeName
            LoserName = AwayName 
            WinnerStr = HomeTemp
            LoserStr = AwayTemp
        #If Number is less than Prob do the same as if statement but flip home and away
        elif Number < Prob:
            Away[0].Stre = HomeTemp + AwayTemp
            Away.append(Away[0])
            Away.pop(0)
            Home.pop(0)
            Description = '"' + AwayName + '(' + str(AwayTemp) + ') for team ' + str(AwayTeam) + ' beat ' + HomeName + '(' + str(HomeTemp) + ') for team ' + str(HomeTeam) + '"'
            WinnerName = AwayName
            LoserName = HomeName
            WinnerStr = AwayTemp
            LoserStr = HomeTemp
        
        #The SQL command, will add all information about the fight to the SQL table Season1
        Command = 'INSERT INTO season1 VALUES (' + str(id) + ', ' + str(Game) + ', ' + str(FightNum) + ', ' + Description + ', ' + '"Team ' + str(HomeTeam) + '", ' + '"Team ' + str(AwayTeam) + '", ' \
            + '"' + HomeName + '"' + ', '+ '"' + AwayName + '"' + ', ' + str(HomeTemp) + ', ' + str(AwayTemp) + ', ' +  '"' + WinnerName + '", "' + LoserName + '", ' + str(WinnerStr) + ', ' \
            + str(LoserStr) + ', ' + str(HomeProb) + ', ' + str(AwayProb) + ', '
        
       #If both teams are still fighting set the win and loss to zero, since the game is not over then commit command
        if len(Home) != 0 and len(Away) != 0:
            Command = Command + '0, 0);'  
            mycursor.execute(Command)
            DB.commit()
        #If Home lost add the new win loss record for each team to each team, then commit command 
        elif len(Home) == 0 and len(Away) != 0:
            Command = Command + str(AwayTeam) + ', ' + str(HomeTeam) + ');' 
            mycursor.execute(Command)
            DB.commit()
            #Change season1results table to new win loss records then commit
            Command = 'update season1results set Wins = Wins + 1 where Teamid = ' + str(AwayTeam) + ';'
            mycursor.execute(Command)
            DB.commit()
            Command = 'update season1results set Loss = Loss + 1 where Teamid = ' + str(HomeTeam) + ';'
            mycursor.execute(Command)
            DB.commit()
        #Same as first elif statement but with away team winning
        elif len(Home) != 0 and len(Away) == 0:
            Command = Command + str(HomeTeam) + ', ' + str(AwayTeam) + ');' 
            mycursor.execute(Command)
            DB.commit()
            Command = 'update season1results set Wins = Wins + 1 where Teamid = ' + str(HomeTeam) + ';'
            mycursor.execute(Command)
            DB.commit()
            Command = 'update season1results set Loss = Loss + 1 where Teamid = ' + str(AwayTeam) + ';' 
            mycursor.execute(Command)
            DB.commit()
        
        #Fight is done so add one the fight number and id 
        FightNum = FightNum + 1
        id = id + 1

    return id

#Loop through 24 fights(The total number of games in a season)    
for i in range(24):
    FightNum = 1
    Round = Fight(ScheduleHome[i], ScheduleAway[i], FightNum, id)
    All = []
    Team1 = []
    Team2 = []
    Team3 = []
    Team4 = []
    #Reset teams after every game 
    mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 1";')

    for k in mycursor:
        Team1.append(Fighter(k[0], k[1]))

    All.append(Team1)

    mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 2";')

    for l in mycursor:
        Team2.append(Fighter(l[0], l[1]))

    All.append(Team2)

    mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 3";')

    for m in mycursor:
        Team3.append(Fighter(m[0], m[1]))

    All.append(Team3)

    mycursor.execute('select Fighter_Name, Strength from teams where Team_Name = "Team 4";')

    for n in mycursor:
        Team4.append(Fighter(n[0], n[1]))
    All.append(Team4)
    
    id = Round
    Game = Game + 1 