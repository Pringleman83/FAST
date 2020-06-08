# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:30:31 2019

@author: david
"""

# Functions and common variables
"""
import os #For file operations
import urllib #For web downloads
import csv #For basic file handling and cleansing before using Pandas
import filecmp #For comparing files
"""
import pandas as pd #For data analysis
from datetime import datetime, timedelta #For date and time management
import os

now = datetime.now()
current_year = now.year
loaded_data = {}#Keys: "League from leagues"+" "+"Season from seasons"
merged_data = pd.DataFrame()
fixtures = pd.DataFrame()
predictions = pd.DataFrame()
prediction_df = pd.DataFrame()
#Configuration
current_english_season = ""
cleanse_detail = 0

# Variables

#File directories
root_dir = os.path.dirname(os.path.realpath(__file__))
raw_data_dir = root_dir + "\\downloaded_files\\raw\\"
clean_data_dir = root_dir + "\\downloaded_files\\clean\\"
unprocessed_predictions_dir = root_dir + "\\predictions\\unprocessed\\"
processed_predictions_dir = root_dir + "\\predictions\\processed\\"
old_preprocessed_predictions_dir = root_dir + "\\predictions\\pre-processed\\"
temp_files_dir = root_dir + "\\temp_files\\"
accumulative_analysis_method_dir = root_dir + "\\analysis\\accumulative_prediction_analysis\\by_method\\"
accumulative_analysis_type_dir = root_dir + "\\analysis\\accumulative_prediction_analysis\\by_type\\"
accuracy_analysis_dir = root_dir + "\\analysis\\accuracy_reporting\\"
method_test_analysis_dir = root_dir + "\\analysis\\method testing\\"

problem_characters = [",","ย", "ö", " "]

leagues = {"England Premier League":"E0", "England Championship":"E1",
           "England League 1":"E2", "England League 2":"E3",
           "England Conf":"EC"}
seasons = {"1993-1994":"9394", "1994-1995":"9495", "1995-1996":"9596",
           "1996-1997":"9697", "1997-1998":"9798", "1998-1999":"9899",
           "1999-2000":"9900", "2000-2001":"0001", "2001-2002":"0102",
           "2002-2003":"0203", "2003-2004":"0304", "2004-2005":"0405",
           "2005-2006":"0506", "2006-2007":"0607", "2007-2008":"0708",
           "2008-2009":"0809", "2009-2010":"0910", "2010-2011":"1011",
           "2011-2012":"1112", "2012-2013":"1213", "2013-2014":"1314",
           "2014-2015":"1415", "2015-2016":"1516", "2016-2017":"1617",
           "2017-2018":"1718", "2018-2019":"1819", "2019-2020":"1920"}

seasons_with_no_EC = ["1993-1994","1994-1995","1995-1996","1996-1997",
                      "1997-1998","1998-1999","1999-2000","2000-2001",
                      "2001-2002","2002-2003","2003-2004","2004-2005"]

seasons_with_all_leagues = ["2005-2006","2006-2007","2007-2008","2008-2009",
                            "2009-2010","2010-2011","2011-2012","2012-2013",
                            "2013-2014","2014-2015","2015-2016","2016-2017",
                            "2017-2018","2018-2019","2019-2020"]

#Dictionary of team with alternative names
#IF ADDING AN ALIAS FOLLOWING AN ERROR, ENSURE THE FIXTURE LIST IS REDOWNLOADED
#AS THE ALIAS LIST IS ONLY USED DURING FILE CLEANSING.
team_aliases = {"Man City":["Manchester City"],
                "Man United":["Manchester Utd"],
                "Sheffield United": ["Sheffield Utd"],
                "Nott'm Forest":["Nottingham"],
                "Sheffield Weds":["Sheffield Wed"],
                "Fylde":["AFC Fylde"]}

#Create a list of alternative names that can be checked against when cleaning
#raw files
alias_list = []
for aliases in list(team_aliases.values()):
    alias_list += aliases
    
#loaded_leagues = {}
loaded_seasons = {}

team_list = []
fixture_team_list = []
team_objs = {}
fix_objs = {}
league_objs = {}
available_columns = []
columns = ["Div", "Date", "HomeTeam", "FTHG", "AwayTeam", "FTAG"]
errors = []
        
download_updates = False

import predictive_functions2 as pf

def general_menu(items):
    """ Takes a list.
    Offers it as options for the user to select from.
    Returns the selected value."""
    if not items:
        print("Error: Menu with no items")
        return 0
    new_list = []
    for number, item in enumerate(items, 1):
        print(number, item)
        new_list.append(item)
    while True:
        try:
            option = 0
            option = int(input("Please select a number from above.\n"))
        except:
            print("Please select a valid option")
        else:
            if option > 0  and option <= len(items):
                break
            else:
                print("Selection out of range. Please select a valid option.")
    print(new_list[option-1])
    return new_list[option-1]
    
def multi_pick(items, selected_items = []):
    """
    Takes a list of items to choose from and an optional list of already
    selected items.
    Offers it as options for the user to choose from.
    By selecting an item it is marked as selected.
    By selecting it again it is marked as unselected.
    By typing "all", all items are selected.
    By typing "none", no items are selected.
    Typing "done" indicates the selection process is complete.
    Selected items are marked "SELECTED"
    Returns a list of selected items."""
    #DEBUG
    #print("Items")
    #print(items)
    #print()
    #print("Selected Items")
    #print(selected_items)
    
    def print_items(items, selected_items):
        for number, item in enumerate(items, 1):
            print(number, item, end="")
            if item in selected_items:
                print(" SELECTED")
            else:
                print()

    while True:
        print_items(items, selected_items)
        option = input("\nPlease select a number from above.\nType \"all\" for all and \"none\" for none.\nType \"done\" when done.\n")
        try:
            option = int(option)
        except:
            if option.lower() == "all":
                for item in items:
                    if item not in selected_items:
                        selected_items.append(item)
            elif option.lower() == "none":
                selected_items = []
            elif option.lower() == "done":
                return selected_items
            else:
                print("Unexpected selection. Please try again.")
        else:
            if option>0  and option<=len(items):
                if items[option-1] in selected_items:
                    selected_items.remove(items[option-1])
                else:
                    selected_items.append(items[option-1])
            else:
                print("Selection out of range. Please select a valid option.")
                
def get_season_key(season_code):
    """
    Takes a 4 digit string league code. (Will remove "-" from a 5 digit code
    but will also warn as this could cause hidden errors)
    Returns the associated key from league_data dictionary.
    """
    if "-" in season_code:
        print ("Removing hypthen")
        season_code = season_code.replace("-","")
    for key, code in seasons.items():
        if code == season_code:
            return key
    print("get_season_key function - Season key not found in seasons dictionary")
    return 1

def get_pred_type_method_keys(pred_function):
    """
    Takes a predictive function.
    Searches through the dictionary of types and functions.
    Returns the type and method keys
    """

    for pred_type, pred_method in pf.predictive_methods.items():
        for method,function in pred_method.items():
            if function == pred_function:
                return (pred_type, method)
    print("get_pred_type_method_keys function - "+
          "key not found in predictive_methods dictionary")
    return 1

def get_team_from_alias(alias):
    for team, aliases in team_aliases.items():
        if alias in aliases:
            return team
    print("get_team_from_alias function - alias not found in team_aliases " +
          "dictionary.")

def get_latest_league(team_name):
    """
    Takes a team name in the form of a string.
    Returns the latest league they've belonged to.
    If the team is not in a league this season, "Not in loaded leagues"
    returned.
    """
    for league in leagues:
        this_season = get_season_key(current_english_season)
        #Check league has been loaded before searching the league for the team
        if league + " " + this_season in loaded_data.keys():
            if team_name in (
                    loaded_data[league + " " + this_season]["HomeTeam"].unique()
                    ) or team_name in (
                            loaded_data[league+" " + this_season]["AwayTeam"].unique()):
                return league
    #Team not found in leagues
    return "Not in loaded leagues"

def one_argument(a=0,b=[]):
        """
        Takes an optional int and a list.
        Checks that only one of the two available arguments have been passed.
        Returns True if ok.
        Returns False if not.
        """
                
        #If both arguments are passed display an error and return 1
        if a and b:
            print("Two parameters passed. Can only use one.")
            return False
        #If no arguments are passed display an error and return 1
        elif (not a) and (not b):
            print("No parameters passed. Must use one.")
            return False
        #If one argument passed return True
        else:
            return True

def get_number(low=1, high=20000):
    number = ""
    accept = False
    while accept == False:
        number = input()
        try:
            number = int(number)
        except:
            print("Please enter a valid number.")
            
        if type(number) == int:
            if ((number < low) or (number > high)):
                print("Please enter a number that is higher than " +
                      str(low) + " and lower than " + str(high+1) + ".")
            else:
                accept = True          
    return number

def previous_encounters(home_team, away_team, h_a_specific):
    """
    Takes home team, away team as strings and home away specific as a boolean.
    Home team and away team are team names.
    If home_away_specific is True. returns a list of results where
    the home team played the away team at home.
    If it's False, returns all previous encounters)
    """
    if h_a_specific:
        return merged_data.loc[(merged_data["HomeTeam"] == home_team) &
                               (merged_data["AwayTeam"] == away_team)][["Date",
                               "HomeTeam","FTHG","FTAG","AwayTeam"]]
    if not h_a_specific:
        return merged_data.loc[((merged_data["HomeTeam"] == home_team) | 
                (merged_data["HomeTeam"] == away_team)) & (
                        (merged_data["AwayTeam"] == away_team) | 
                        (merged_data["AwayTeam"] == home_team))][["Date",
                        "HomeTeam","FTHG","FTAG","AwayTeam"]]

#############################################################################
###Work in progress
#############################################################################
def display_results(number_of_games=1, leagues=[],
                    seasons=[current_english_season]):
    pass

def display_fixtures(selected_leagues=leagues, teams=team_list):
    print("Fixtures")
    #Go through all selected leagues
    for league in selected_leagues:
        #Get the league code (leagues[league]). If it's in the DIv column of
        #fixtures display the leagues fixtures that include the selected teams
        

        if leagues[league] in list(fixtures.Div.unique()):
            print("\n" + league)
            
            #Create a new dataframe for this league only
            league_fix_df = fixtures[fixtures["Div"] == leagues[league]]
            
            if league_fix_df.empty:
                continue
            
            #Print each fixture where the home team or away team are in the
            #teams list (by default, all teams are in the teams list).
            
            print(league_fix_df[league_fix_df["HomeTeam"].isin(teams) | 
                    league_fix_df["AwayTeam"].isin(teams)]
                    [["Date","Time","HomeTeam","AwayTeam"]])
            
    
        else:
            continue
    #print fixtures for that league if one of the teams are in the teams list.