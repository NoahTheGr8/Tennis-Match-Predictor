# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 01:47:23 2020

@author: R Noah Padilla

Problem type: Multi-Label Classification

- * Clean Data
- Choose an Algo (KNN, ForestClassifier, MLPClassifier)
- train and test
"""

import pandas as pd
import numpy as np

from utils import *


'''
cleanData(dataframe list) > where each dataframe is a years worth of tennis tournaments

'''
def cleanData(All_Data):
    print("Initialized data cleaning...")
    
    
    #>>>>>>>>Total IDS
    tour2015 =  All_Data[0]
    allIDS2015 = tour2015[1:,0] #contains all IDS of the tournament, contains repeated values
    print("using ID before set transform - ",len(allIDS2015))
    allIDS2015 = set(allIDS2015)
    print("using ID after set transform - ", len(allIDS2015))
    
    #>>>>>>>>Total Finals
    allRounds2015 = tour2015[1:,25] #all rounds in the tournament
    totFinals2015 = np.where(allRounds2015 == 'F')
    print("Total number of finals", len(totFinals2015[0]))
    
    #>>>>>>>>Total RRs
    totRRs = 0
    IDS_visited = [] #array stored to keep track of which IDS visited when calculating total round robin tourneys
    #go thru the rows only
    for i in range(1,len(tour2015)):
        
        if (tour2015[i,0] in allIDS2015) and (tour2015[i,0] not in IDS_visited) and (tour2015[i,25] == 'RR'):
            IDS_visited.append(tour2015[i,0])
            totRRs += 1
    
    print("Total number of RR's", totRRs)
    '''
    total finals = 67 exluding round robin
    total RR = 
    '''
    
    
    #TODO - Consider round robin? MAybe? consider how it adds to their wins and stats so map tourney to winner and get all of winners stats like all wins no matter format
    
    return -1,-1


if __name__ == "__main__":

    print(" >>> Tennis Tournament Predictor <<<")
    
    '''
    Get the raw data and clean it out:
        > For each tournament have 1 output
        > For each tournament - keep the winners attributes
    
    '''
    
    #Do most recent past 5 years
    Data_2015 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2015.csv',header=None).to_numpy()
    Data_2016 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2016.csv',header=None).to_numpy()
    Data_2017 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2017.csv',header=None).to_numpy()
    Data_2018 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2018.csv',header=None).to_numpy()
    Data_2019 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2019.csv',header=None).to_numpy()
    Data_2020 = pd.read_csv('..//Tennis-Tournament-Predictor//tennis_atp-master//atp_matches_2020.csv',header=None).to_numpy()
    
    
    All_Data = []
    All_Data.append(Data_2016)
    All_Data.append(Data_2017)
    All_Data.append(Data_2018)
    All_Data.append(Data_2019)
    All_Data.append(Data_2020)
    
    '''
    > Create a set containing all players names in a set
    > Sort set
    >Parse each tournament
    > Use the set to ONEHOT encode each tournament
    '''
    
    #Extract import features and onehot encode all the values
    X,y = cleanData(All_Data)
    
    
    