# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 19:34:49 2019

@author: david
"""
# Imports
import os
import pandas as pd
import common_functions as c
import urllib #For web downloads
import time #For delays
import filecmp #For comparing files
import csv #For basic file handling and cleansing before using Pandas
import menus
from team2 import Team
from league2 import League
"""
#from fixture import Fixture
import common as c
import predictive_functions as pf
import prediction_analysis as pa
"""
#Variables

#Selections
selected_leagues = ['England Premier League',
                    'England Championship',
                    'England League 1',
                    'England League 2',
                    'England Conf']

selected_seasons = ['2019-2020','2018-2019','2017-2018','2016-2017',
                    '2015-2016','2014-2015','2013-2014','2012-2013',
                    '2011-2012','2010-2011','2009-2010','2008-2009',
                    '2007-2008','2006-2007','2005-2006','2004-2005',
                    '2003-2004','2002-2003','2001-2002','2000-2001',
                    '1999-2000','1998-1999','1997-1998','1996-1997',
                    '1995-1996','1994-1995','1993-1994']

#Functions
def intro():
    fast_f="ootball "
    fast_a="nalysis "
    fast_s="election"
    fast_t="ool     "
    
    print("\n\nWelcome to F.A.S.T.")
    for i in range(len(fast_f)):
        print("           "+fast_f[i]+" "+fast_a[i]+" "+fast_s[i]+" "+fast_t[i])
    print()

def read_config():
    #Reads the config.txt file and returns a list of variables
    print("Loading configuration...") #Status
    for line in open("config.txt"):
        #Skip comments
        if line[0] == "#":
            continue

        if line.split(":")[0] == "Current English season":
            current_english_season = line.split(":")[1][1:5]
            continue
        if line.split(":")[0] == "Display data cleansing information":
            cleanse_detail = int(line.split(":")[1][1:2])
            continue
    print("Configuration loaded.") #Status
    return(current_english_season, cleanse_detail)
    
def download_missing_files(download_updates, current_english_season,
                           cleanse_detail, problem_characters):
    """
    Takes the download_updates boolean.
    
    """
    print ("Checking for missing files...") #Status
    #For every line in the file
    for url in open("urls.txt"):
        #Skip comments in the url file
        if url[0] == "#":
            continue
        #Split on the rightmost / and take everything on the right side of that
        name = (url.rsplit("/", 2)[-2] + "_" +
                url.rsplit("/", 2)[-1][:-1]) #[:-1]removes \n from end of line.
        
        #Combine the name and the downloads directory to get the local filename
        #Also do the same for the temporary directory for files that already exist
        filename = os.path.join(c.raw_data_dir, name)
        temp_filename = os.path.join(c.temp_files_dir, name)
        
        #Number of times to retry downloads that fail
        number_of_attempts = 3    
        
        #Download file if:
            #it doesn't exist
            #it's the current season and download updates is True
            #it's the fixture list
        if ((not os.path.isfile(filename)) or 
            (name[0:4] == current_english_season and download_updates)
            or (url.strip() == "https://www.football-data.co.uk/fixtures.csv" 
                and download_updates)):
            while number_of_attempts > 0:
                try:
                    
                    #If file already exists, download to a temporary location
                    #and set exists flag to True.
                    #Don't show the file that is being downloaded.
                    if (os.path.isfile(filename)):
                        exists = True
                        urllib.request.urlretrieve(url[:-1], temp_filename)
                    
                    #Otherwise, download to raw_data and set exists flag to False.
                    #Also show the file that is being downloaded
                    else:
                        exists = False
                        print("Downloading " + name + "...")
                        urllib.request.urlretrieve(url[:-1], filename)
                        
                    #print("File: " + name + " downloaded successfully.")
                    time.sleep(0.1)
                except:
                    #On fail of download, advise, and try again if retries left.
                    number_of_attempts -= 1
                    #Say "attempts" for more than one or "attempt" for one
                    if number_of_attempts != 1:
                        plural = "s"
                    else:
                        plural = ""
                    print("Error downloading " + name + ". " + 
                          str(number_of_attempts) + " attempt" + plural +
                          " remaining.")
                else:
                    #If download was a success
                    #If the file already exists, run a comparison before replacing.
                    if exists:
                        #If no errors, check if file is same as existing file
                        if filecmp.cmp(temp_filename, filename):
                            #print(name + " is not a new file")
                            os.remove(temp_filename)
                            break
                        else:
                            print("New file: " + name)
                            os.remove(filename)
                            os.rename(temp_filename, filename)
                            print("Cleansing " + filename)
                            cleanse_data(filename, name, cleanse_detail,
                                         problem_characters)
                            break        
                    else:
                        #Cleanse data
                        print("Cleansing " + filename)
                        cleanse_data(filename, name, cleanse_detail,
                                     problem_characters)
                        break
                        
    print("File check complete.") #Status

def cleanse_data(file, filename, cleanse_detail, problem_characters):
    if cleanse_detail:
        print("Working with " + filename + "...")
    
    """user_in = input()
    if user_in == "q":
        break"""
    
    new_file = []
    with open(file) as original:
        csv_file = csv.reader(original, delimiter = ",")
        row_count = 0
        for row in csv_file:
            if row_count == 0:
                home_team_index = row.index("HomeTeam")
                away_team_index = row.index("AwayTeam")
                #Add a new header for season - useful for merged dataframes
                row.insert(0, "Season")
                
                #Get accurate count for headers:
                header_count = 0
                for header in row:
                    if header:
                        header_count += 1
                        
                if header_count != len(row):
                    if cleanse_detail:
                        print("Length mismatch")
                        print("Old row: ")
                        print(row)
                        print("Fixed row: ")
                    row = row[:header_count]
                    if cleanse_detail:
                        print(row)
                    
                if "Referee" in row:
                    ref_index = row.index("Referee")
                    if cleanse_detail:
                        print("Referee index for this sheet is: " +
                              str(ref_index))
                    row_count += 1
                    ref_check = True

                else:
                    if cleanse_detail:
                        print("No referee header in this file")
                    ref_check = False
                    row_count += 1
            else:
                #Debug - Target a specific row
                """if count < 500:
                    count += 1
                    continue"""
                
                #Check team aliases
                
                #DEBUG
                #print("DEBUG " + row[home_team_index] + " - " + row[away_team_index])
                #END OF DEBUG
                
                if row[home_team_index] in c.alias_list:
                    #DEBUG
                    #print(row[home_team_index])
                    #input()
                    #END OF DEBUG
                    
                    for alias_list in list(c.team_aliases.values()):
                        for alias in alias_list:
                            if row[home_team_index] == alias:
                                row[home_team_index] = c.get_team_from_alias(
                                        row[home_team_index])
                    #DEBUG
                    #print(row[home_team_index])
                    #input()
                    #END OF DEBUG
                if row[away_team_index] in c.alias_list:
                    #DEBUG
                    #print(row[away_team_index])
                    #input()
                    #END OF DEBUG
                    for alias_list in list(c.team_aliases.values()):
                        for alias in alias_list:
                            if row[away_team_index] == alias:
                                row[away_team_index] = c.get_team_from_alias(
                                        row[away_team_index])
                    #DEBUG
                    #print(row[away_team_index])
                    #input()
                    #END OF DEBUG
                            
                #Check if row contains any data (delete if empty)
                data_count = 0
                for field in row:
                    if field:
                        data_count += 1
                        continue
                if data_count == 0:
                    row = ""
                
                if row:
                    #Insert the season into the new season column
                    season = str(filename[:2]) + "-" + str(filename[2:4])
                    row.insert(0, season)
                    #Remove blank noise fields from end of row
                    row = row[:header_count]
                    
                #Check the referee field for errors
                #If contains an unsupported character
                if ref_check and row:

                    #If contains a comma
                    if "," in row[ref_index]:
                        if cleanse_detail:
                            print("Error, comma found in row " +
                                  str(row_count) +": " + row[ref_index])
                        temp_field = row[ref_index].split(",")
                        row[ref_index] = temp_field[1][1:] + " " + temp_field[0]
                        if cleanse_detail:
                            print("Fixed referee field in row " +
                                  str(row_count) + ": " + row[ref_index])
                            print("New row:")
                            print(row)
                
                #Check all fields for non unicode characters
                if cleanse_detail:
                    print("Checking for non unicode characters...")
                
                field_count = 0
                for field in row:
                    for problem in problem_characters:
                        if problem in field:
                            
                            if cleanse_detail:
                                print("Non unicode character found in row " +
                                      str(row_count))
                            row[field_count] = field.replace(problem,"")
                            if cleanse_detail:
                                print("Non unicode character removed.")
                                print("New row: ")
                                print(row)
                    field_count += 1    
                row_count += 1  
            #Write row to new file list
            new_file.append(row)
    fixed = open(c.clean_data_dir+filename, "w+")
    for record in new_file:
        item_count = 0
        for item in record:
            fixed.write(item)
            if item_count != len(record) - 1:
                fixed.write(",")
            else:
                fixed.write("\n")
            item_count += 1           
    fixed.close()
    
def cleanse_raw_data(cleanse_detail = 0):
    """
    Used for debugging the cleansing function without the need to redownload
    raw data.
    """
    for file_name in os.listdir(c.raw_data_dir):
        if cleanse_detail:
            print("Cleansing: ")
            print("file_path: " + c.raw_data_dir + file_name)
            print("file_name: " + file_name)
        cleanse_data(c.raw_data_dir + file_name, file_name)
        if cleanse_detail:
            print("Done.")
            
def load_data(selected_leagues, selected_seasons):
    merged_data = pd.DataFrame()
    loaded_data = {}
    if selected_seasons and selected_leagues:
        for league in selected_leagues:
            #print(league) #DEBUG
            for season in selected_seasons:
                #print(season) #DEBUG
                #loaded_data[league+" "+season] = csv.DictReader(open(file_dir+
                #"\\"+seasons[season]+"_"+leagues[league]+".csv"))
                
                #DEBUG CODE
                #print(league)
                #print(file_dir+"\\"+seasons[season]+"_"+leagues[league]+".csv")
                #input()
                
                ##############################################
                """This is to prevent the attempt of loading EC data
                for seasons when EC data wasn't recorded."""
                if league == "England Conf" and season in c.seasons_with_no_EC:
                    continue
                ##############################################
                try:
                    loaded_data[league + " " + season] = pd.read_csv(
                            c.clean_data_dir+"\\" + c.seasons[season] + 
                            "_" + c.leagues[league] + ".csv")
                    
                except Exception as e:
                    print("ERROR " + season + "_" + league + " Error: " + 
                          str(e))
                    c.errors.append([season + "_" + league, str(e)])
                    continue
                
                #Update available columns
                #input("Update cols")#DEBUG CODE
                for col in loaded_data[league + " " + season]:
                    if col not in c.available_columns:
                        c.available_columns.append(col)
                
                #Create a league object for this league and season
                c.league_objs[league + " " + season] = League(league, season)
        
        #Create the merged_data dataframe
        merged_data = pd.concat(list(loaded_data.values()), sort=False)
        #Convert dates in merged_data to datetime objects
        merged_data["Date"] = pd.to_datetime(merged_data["Date"],
                     dayfirst=True)
        #Sort merged data by date descending (important for gathering data from a set number of games going back)
        merged_data = merged_data.sort_values(by="Date", ascending=False)
        
        #Create list of teams
        for team in pd.concat([merged_data["HomeTeam"],merged_data["AwayTeam"]]):
            if team not in c.team_list:
                c.team_list.append(team)
        c.team_list.sort()
        
        #Create team objects (Can't be done at same time as list
        #creation as the loaded_data doesn't contain all leagues.
        print("Creating team objects")#DEBUG
        for team in c.team_list:
            c.team_objs[team] = Team(team)

        print("done")
        
        if not c.errors:                
            print("Data loaded successfully.\n") #Status
        else:
            print("\nThere were errors with the following files: \n")
            for error in c.errors:
                print(error[0])
            print("\nAvoid using these files until the errors have been fixed.\n")
        
        print("Loading fixtures")
        try:
            c.fixtures = pd.read_csv(c.clean_data_dir + "\\www.football-data.co.uk_fixtures.csv")
            
            #Convert dates in c.fixtures to datetime objects
            c.fixtures["Date"] = pd.to_datetime(c.fixtures["Date"],
                     dayfirst=True)
            
            #Create a list of teams from the fixture list)
            temp_fixture_team_list = (list(c.fixtures.HomeTeam.unique()) +
                                   list(c.fixtures.AwayTeam.unique()))
            #Add teams that are loaded into the app and in the fixture list
            #to the fixture_team_list. This means that teams  where no league
            #data is loaded aren't included.
            for team in c.team_list:
                if team in temp_fixture_team_list:
                    c.fixture_team_list.append(team)
        except Exception as e:
                print("ERROR LOADING FIXTURES - Error: " + str(e))
                c.errors.append(["Fixtures", str(e)])
        print("Done")
        return [loaded_data, merged_data]

    elif (not c.selected_seasons) and (not c.selected_leagues):
        print("***Select leagues and seasons to load first.***")
    elif not c.selected_seasons:
        print("***Select seasons to load first.***")
    elif not c.selected_leagues:
        print("***Select leagues to load first.***")

def main():
    #Main code  
    intro()
    
    #Create data directories if they don't already exist
    if not os.path.exists(c.raw_data_dir):
        os.makedirs(c.raw_data_dir)   
    if not os.path.exists(c.clean_data_dir):
        os.makedirs(c.clean_data_dir)       
    if not os.path.exists(c.unprocessed_predictions_dir):
        os.makedirs(c.unprocessed_predictions_dir)       
    if not os.path.exists(c.processed_predictions_dir):
        os.makedirs(c.processed_predictions_dir)        
    if not os.path.exists(c.old_preprocessed_predictions_dir):
        os.makedirs(c.old_preprocessed_predictions_dir)        
    if not os.path.exists(c.temp_files_dir):
        os.makedirs(c.temp_files_dir)
    if not os.path.exists(c.accumulative_analysis_method_dir):
        os.makedirs(c.accumulative_analysis_method_dir)
    if not os.path.exists(c.accumulative_analysis_type_dir):
        os.makedirs(c.accumulative_analysis_type_dir)
    if not os.path.exists(c.accuracy_analysis_dir):
        os.makedirs(c.accuracy_analysis_dir)
    if not os.path.exists(c.method_test_analysis_dir):
        os.makedirs(c.method_test_analysis_dir)
    
    
    #Read settings from congif file
    config = read_config()
    c.current_english_season = config[0]
    cleanse_detail = config[1]
    
    #Ask if it's necessary to download the latest files
    dl_latest = input("Would you like to download the latest files for this"
                      + " season? (Y/N)\n")
    if dl_latest.lower() == "y" or dl_latest.lower() == "yes":
        download_updates = True
    else:
        download_updates = False
        
    download_missing_files(download_updates, c.current_english_season,
                           cleanse_detail, c.problem_characters)
    run = True
    while(run):
        selected_seasons = menus.select_seasons(c.current_english_season,
                                                c.seasons)
        if selected_seasons == "exit":
            break
        data = load_data(selected_leagues, selected_seasons)
        

        
        c.loaded_data, c.merged_data = data
        
        #Populate dictionary of loaded seasons
        for season in list(c.merged_data["Season"].unique()):
            c.loaded_seasons[c.get_season_key(season.replace("-",""))] = (
                    season)
            
        menus.main_menu()

main()