import mysql.connector

#Connect to mySQL database
DB = mysql.connector.connect(host=Host, user=User,passwd=PassWord, database=DataBase)
mycursor = DB.cursor()

#Function that returns most number of fights a single fighter has appeared in
def MostFights():
    mycursor.execute('select max(fight) from season1 where fight = (select max(fight) from season1);')
    for a in mycursor:
        return a[0]

#Function that returns least number of fights a single fighter has appeared in        
def MinFights():
    mycursor.execute('select min(fight) from season1 where fight = (select min(fight) from season1 where win > 0 or loss > 0);')
    for b in mycursor:
        return b[0]
        
#Function that return the most number of fights won by a single fighter
def MostFighterWins():
    mycursor.execute('select Winner, count(Winner) from season1 group by Winner;')
    #Keeps track of max value
    Max = 0
    #Keeps track of current interation
    Iter = 0
    for c in mycursor:
        #If current value is higher than the current max value, max value becomes current value
        if(c[1] > Max):
            Max = c[1]
        Iter = Iter + 1
    return Max
    
#Function that return the most number of fights lost by a single fighter
def MostFighterLosses():
    mycursor.execute('select Loser, count(Loser) from season1 group by Loser;')
    #Keeps track of max value
    Max = 0
    #Keeps track of current interation
    Iter = 0
    for c in mycursor:
        #If current value is higher than the current max value, max value becomes current value
        if(c[1] > Max):
            Max = c[1]
        Iter = Iter + 1
    return Max
    
#Function that returns the highest strength achieved by a fighter
def MostStr():
    mycursor.execute('select max(greatest(Winner_str, Loser_str)) from season1;')
    for e in mycursor:
        return e[0]
        
#Function that returns smallest percantage chance of winning, and still won the fight 
def BiggestUpset():
    mycursor.execute('select max((least(Home_prob, Away_Prob)))  from season1 where winner_str < loser_str and (Away_Prob = (select max(greatest(Home_prob, Away_prob))' 
    'from season1 where Winner_Str < Loser_Str) or Home_Prob = (select max(greatest(Home_prob, Away_prob)) from season1 where Winner_Str < Loser_Str));')
    for f in mycursor:
        return f[0]
        
#Function that returns longest streak of fight won by a fighter
def LongestStreak():
    Names = []
    #Current streak for individual fighter
    LongCur = 0
    #Overall longest streak for indiviual fighter
    LongInd = 0
    #Longest streak of all fighters
    Long = 0
    #Saves names in order of fight wins, so function can check win streak name by name 
    mycursor.execute('select Winner, count(Winner) from season1 group by Winner order by count(Winner) desc;')
    for g in mycursor:
        Names.append(g[0])
    #Go through all fights of all fighters, one-by-one    
    for h in Names:
        mycursor.execute('select Winner from season1 where Winner = "' + h + '" or Loser = "' + h + '";')
        for i in mycursor:
            #If fighter won add one to current streak, LongCur
            if(i[0] == h):
                LongCur = LongCur + 1
            #If fighter lost, check if current streak is longer than overall streak
            else:
                #Change fighters overall streak to current streak, if current streak is longer, then reset current streak
                if(LongCur > LongInd):
                    LongInd = LongCur
                LongCur = 0
        #After overall fighter streak is found, compare to streak for all fighters, if fighter streak is longer than overall streak, change to fighters streak 
        if(LongInd > Long):
            Long = LongInd
        LongInd = 0
    return Long 
    
#Opens new text file and writes records, to prepare to save all records to this file
file1 = open("C:/Users/Owner/Desktop/Projects/Gladiator/Records.txt", "w")
file1.write('Records:\n')
file1.close()

#Opens and writes all the records on text file
file1 = open("C:/Users/Owner/Desktop/Projects/Gladiator/Records.txt", "a")
file1.write('Most Fights: ' + str(MostFights()) + '\n')
file1.write('Least Fights: ' + str(MinFights()) + '\n')
file1.write('Most Fighter Wins: ' + str(MostFighterWins()) + '\n')
file1.write('Most Fighter Losses: ' + str(MostFighterLosses()) + '\n')
file1.write('Highest Strength: ' + str(MostStr()) + '\n')
file1.write('Biggest Upset: ' + str(BiggestUpset()) + '\n')
file1.write('Longest Streak: ' + str(LongestStreak()) + '\n')

#Close text file 
file1.close()