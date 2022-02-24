# Gladiator
In this project I use python and SQL to test the game theory game of gladiators proposed in Haim Shapira's book "Gladiators, Pirates and Games of Trust: How Game Theory, Strategy and Probability Rules over our lives."

Originally a project to test the probablity theory of the game, I decided to instead create a season of this game and save the data to a MySQL server and pull data from it to find information on the season so that I could practice my SQL skills. 

The premise of the game is that two teams of fighters face off, each with thier own strength value. The chance of a fighter winning is their strength divided by the combine strengths of both fighters. The winner of the fight then gains the strength of the other fighter and goes to the end of the line up. This goes until one team runs out of fighters. The point of this game is to show that the lineup don't matter, that the chance of a team winning will always be the combined strength of the team, divided by the combined strength of both teams. 

GladiatorTeams.py contains the code used to create the four teams I used when running the season, then saves the information to the MySQL server.

GladiatorSeason.py run the games for the entire season, using the teams created from GladiatorTeams.py then saves all the results to the MySQL server.

GladiatorRecords.py then queries the GladiatorSeason.py table to find different records that were set in the season. It then saves that information to the text file Records.txt. 
