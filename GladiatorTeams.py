import numpy
import mysql.connector

#Connect to mySQL database
DB = mysql.connector.connect(host=Host, user=User,passwd=PassWord, database=DataBase)
MyCursor = DB.cursor()

#Create class for each fighter that contains name and value of its strength
class Fighter:
    def __init__(self, Name, Stre):
        self.Name = Name
        self.Stre = Stre

#Array of names to be randomly chosen from for each team 
Names = ['Bob', 'Bill', 'Joe', 'Jack', 'James', 'Ryan', 'Aaron', 'Katie', 'Matt', 'David', 'Dan', 'Tyler', 'Alex'
         'Nate', 'John', 'Connor', 'Isaac', 'Hannah', 'Karl', 'Tom', 'Frank', 'Jim', 'Steve', 'Josh', 'Tim', 'Ashley'
         'Randall', 'Adam', 'Andy', 'Abe', 'Jeremy', 'Dalton', 'Riley', 'Ricky', 'Felix', 'Frank', 'Kurt', 'Kirk',
         'Amy', 'Brandon', 'Jesse', 'Mark']

#Initialize arrays that will contain all the Fighter objects for each team         
Team1 = []
Team2 = []
Team3 = []
Team4 = []

#Initialize values for total strength of each team
Team1Str = 0
Team2Str = 0
Team3Str = 0
Team4Str = 0

#For loop that creates info for each team. Each team has ten players. A name for each player will be randomly selected
#from Names and then removed so it doesn't repeat. Then a random strenght value will be selected for fighter between 50 
#and 250. Add each fighters strength value to get total team strength value. Do a for loop for each of four teams
for i in range(10):
    TempName = Names[numpy.random.randint(0, (len(Names)))]
    TempStr = numpy.random.randint(50, 250)
    Team1.append(Fighter(TempName, TempStr)) 
    Names.remove(TempName)
    Team1Str = Team1Str + TempStr

for i in range(10):
    TempName = Names[numpy.random.randint(0, (len(Names)))]
    TempStr = numpy.random.randint(50, 250)
    Team2.append(Fighter(TempName, TempStr)) 
    Names.remove(TempName)
    Team2Str = Team2Str + TempStr

for i in range(10):
    TempName = Names[numpy.random.randint(0, (len(Names)))]
    TempStr = numpy.random.randint(50, 250)
    Team3.append(Fighter(TempName, TempStr)) 
    Names.remove(TempName)
    Team3Str = Team3Str + TempStr

for i in range(10):
    TempName = Names[numpy.random.randint(0, (len(Names)))]
    TempStr = numpy.random.randint(50, 250)
    Team4.append(Fighter(TempName, TempStr)) 
    Names.remove(TempName)
    Team4Str = Team4Str + TempStr

#Initialize command value. Will contain string that will be a sql command 
Command = ''
#Used for primary key id 
num = 1
#Create SQL command for each team
for thing in Team1:
    Command = 'INSERT INTO teams VALUES (' + str(num) + ', "Team 1", ' + '"' + thing.Name + '"' + ', ' + str(thing.Stre) + ', ' + str(Team1Str) + ');'
    #Executes SQL command
    mycursor.execute(Command)
    #Commits command
    DB.commit()
    #Adds one the primary key id 
    num = num + 1
    
for thing in Team2:
    Command = 'INSERT INTO teams VALUES (' + str(num) + ', "Team 2", ' + '"' + thing.Name + '"' + ', ' + str(thing.Stre) + ', ' + str(Team2Str) + ');'
    mycursor.execute(Command)
    DB.commit()
    num = num + 1

for thing in Team3:
    Command = 'INSERT INTO teams VALUES (' + str(num) + ', "Team 3", ' + '"' + thing.Name + '"' + ', ' + str(thing.Stre) + ', ' + str(Team3Str) + ');'
    mycursor.execute(Command)
    DB.commit()
    num = num + 1

for thing in Team4:
    Command = 'INSERT INTO teams VALUES (' + str(num) + ', "Team 4", ' + '"' + thing.Name + '"' + ', ' + str(thing.Stre) + ', ' + str(Team4Str) + ');'
    mycursor.execute(Command)
    DB.commit()
    num = num + 1