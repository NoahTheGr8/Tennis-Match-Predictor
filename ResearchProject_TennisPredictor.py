# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 01:47:23 2020

@author: R Noah Padilla

Problem type: Classification

Goal: Predict a match winner given the previous years statistics
"""

import pandas as pd
import numpy as np
import sys

from utils import *

'''
extractFeatures Algorithm:
    1. Create a 'playerDB' that extracts stats about each player from that particular year
    2. For each line (match in excel sheet) from 2018-2019: ** IGNORE MATCHES THAT ARE INCOMPLETE **
        > Deduce 1 feature per statistic between the 2 players
        > Create a sample and append statistic to dataset X
        > Label the sample (one hot) and append to dataset y
        
        
    Goal - predict match outcome given their history and upcoming match names
    X = [courtstats accumalted over time, acestats from history, etc.]
        
'''

def extractFeatures(allMatches):
    
    '''
    #1. Create a database to make the process easier to find player stats
    playerDB20XX = [name, ATP rank, ATP points,  claywins,hardWins,grassWins, 
                     FS,W1SP,W2SP,WSP,TMW,ACES,DF,BP]
    
    '''
    
    #Get players names that have complete stats
    allPlayers2018 = set([])
    for match in allMatches[0]:
        #Get players names that contain key attributes
        if(not pd.isnull(match[27])) and (not pd.isnull(match[46])) and (not pd.isnull(match[47])) and( not pd.isnull(match[48])):
            allPlayers2018.add(match[10])
            allPlayers2018.add(match[18])
    
    allPlayers2018 = list(sorted(allPlayers2018)) #converted so can help with OH encoding
    print("Total players in 2018", len(allPlayers2018))
    
    playerCount = 0
    playerDB2018 = []
    #Hardcode traversing through 2018 data
    for playerName in allPlayers2018:
        RANK = 0 #since matches are in order from oldest at top to newest at bottom - just keep updating the rank
        POINTS = [] #take the max at the end
        acesPerGame =[] #stores all aces per game - will take avg at end
        dfPerGame = [] #stores all the double faults per game - will take avg at end
        WFS = [] #stores all wons points on first serve per match
        WSS =[] #stores all wons points on second serve per match
        total_svpt = 0 #total times player serves
        total_1stIn = 0 #Total serves that went in
        total_1stWon = 0 #Total first serves that were won
        total_2ndWon = 0 #Total second serves that were won
        total_bpSaved = 0 #total break points won
        total_bpFaced = 0 #total breaks points encountered
        claywins = 0
        hardWins = 0
        grassWins = 0
        totWins = 0
        totLosses = 0
        
        for match in allMatches[0][1:,]:
            #If key attributes are not null then its a match with complete statistics | attribute 27 is a good indicator on whether or not a match has the features we need
            
            if (playerName in allPlayers2018) and (not pd.isnull(match[27])) and (not pd.isnull(match[46])) and (not pd.isnull(match[47])) and( not pd.isnull(match[48])):
                #print(match[27])
                
                #if player is a winner then look in these indices
                if match[10] == playerName:
                    
                    totWins += 1
                    RANK = int(match[45]) 
                    POINTS.append(int(match[46]))
                    acesPerGame.append(int(match[27]))
                    dfPerGame.append(int(match[28]))
                    WFS.append(int(match[31]))
                    WSS.append(int(match[32]))
                    total_svpt += int(match[29])
                    total_1stIn += int(match[30])
                    total_1stWon += int(match[31])
                    total_2ndWon += int(match[32])
                    total_bpSaved += int(match[34])
                    total_bpFaced += int(match[35])
                    
                    if match[2] == 'Clay':
                        claywins += 1
                    if match[2] == 'Hard':
                        hardWins += 1
                    if match[2] == 'Grass':
                        grassWins += 1
                
                #elif player is a loser then look in these other indices
                if match[18] == playerName:
                    totLosses += 1
                    RANK = int(match[47]) 
                    POINTS.append(int(match[48]))
                    acesPerGame.append(int(match[36]))
                    dfPerGame.append(int(match[37]))
                    WFS.append(int(match[40]))
                    WSS.append(int(match[41]))
                    total_svpt += int(match[38])
                    total_1stIn += int(match[39])
                    total_1stWon += int(match[40])
                    total_2ndWon += int(match[41])
                    total_bpSaved += int(match[43])
                    total_bpFaced += int(match[44])
                #print(playerName, match[1], match[6])
        ACES = np.mean(acesPerGame) # Avg aces per game
        FS = total_1stIn / total_svpt #first serve success percentage -> total_1stIn / total_svpt
        W1SA = np.mean(WFS) #Win on first serve average -> np.mean([1stWon_match1,...,1stWon_matchn])
        W2SA = np.mean(WSS) #Win on second serve average -> np.mean([2ndWon_match1,...,2ndWon_matchn])
        WSP =  (total_1stWon + total_2ndWon)/ total_svpt #Overall winning on serve percentage -> (total_1stWon + total_2ndWon) / (total_svpt) 
        TMW = totWins / (totWins + totLosses) #Perentage of all matches won -> totWins / (totWins + totLosses)
        DF =  np.mean(dfPerGame)#Avg number of double faults -> np.mean([df_match1,..df_matchn])
        BP =  total_bpSaved / total_bpFaced #Percentage of break points won -> total_bpSaved/total_bpFaced
        
        currPlayerStats = [playerName, ACES, FS, W1SA, W2SA, WSP,TMW,DF, BP]
        playerDB2018.append(currPlayerStats)
        print("stored data for player", playerCount)
        playerCount += 1
        
    return -1,playerDB2018


if __name__ == "__main__":

    print(" >>> Tennis Tournament Predictor <<<")
    
    '''
    Get the raw data and clean it out:
        > For each tournament have 1 output
        > For each tournament - keep the winners attributes
    '''
    
    #Do most recent past 2 years
    allMatches2018 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2018.csv',header=None).to_numpy()
    allMatches2019 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2019.csv',header=None).to_numpy()
    #allMatches2020 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2020.csv',header=None).to_numpy()
    
    #List containing all the matches from all the years
    allMatches = []
    allMatches.append(allMatches2018)
    allMatches.append(allMatches2019)
    #allMatches.append(allMatches2020)
    
    #Extract features into X and y
    X,y = extractFeatures(allMatches)
    
    
    #split and train the data
    
    
    #compare performance between MLP and Forest
    
    
    
    
    