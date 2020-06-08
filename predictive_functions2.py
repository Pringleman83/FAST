# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:37:01 2019

@author: david
"""
import common_functions as c
import pandas as pd
import os
#import prediction_analysis as pa
from fixture2 import Fixture

def win_draw_1(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 3,
               difference_threshold_home_win = 2.33, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)

def win_draw_2(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 3,
               difference_threshold_home_win = 1.33, 
               difference_threshold_away_win = 1.33,
               difference_threshold_draw = 0.2,
               season=c.current_english_season)
    
def win_draw_3(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 6,
               difference_threshold_home_win = 2.33, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)
    
def win_draw_4(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 9,
               difference_threshold_home_win = 2.33, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)
    
def win_draw_5(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 12,
               difference_threshold_home_win = 2.33, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)
    
def win_draw_6(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.33, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)

def win_draw_7(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2, 
               difference_threshold_away_win = 2,
               difference_threshold_draw = 0.8,
               season=c.current_english_season)

def win_draw_8(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.4, 
               difference_threshold_away_win = 2.4,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)

def win_draw_9(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.5, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)

def win_draw_10(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.6, 
               difference_threshold_away_win = 2.6,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)
    
def win_draw_11(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.6, 
               difference_threshold_away_win = 2.33,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)
    
def win_draw_12(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 15,
               difference_threshold_home_win = 2.6, 
               difference_threshold_away_win = 2,
               difference_threshold_draw = 0.3,
               season=c.current_english_season)

def win_draw_13(fixtures, retrospective=False):
    return win_draw(fixtures, from_date=c.now, show_all_games=True,
               retrospective=retrospective, number_of_games_back = 2,
               difference_threshold_home_win = 3, 
               difference_threshold_away_win = 3,
               difference_threshold_draw = 0.0,
               season=c.current_english_season)

def win_draw(fixtures, from_date=c.now, show_all_games=True,
             retrospective=False, number_of_games_back = 3,
             difference_threshold_home_win = 2.3,
             difference_threshold_away_win = 2.3,
             difference_threshold_draw = 0.3,
             season=c.current_english_season, method = ""):
    """
    Prediction function "Win Draw 1"
    Takes in a dataframe of fixtures
    An optional from_date datetime object to determine when the predictor looks
    back from.
    An optional all_games boolean which determines whether only selections are
    returned or whether all games are returned (for analysis / pattern finding).
    An optional retrospective boolean to indicate whether actual results should
    be returned where games have already been played.
    Compares the home goal difference of the home team with the away goal
    difference of the away team for the last 3 games of each fixture.
    If at least one game meets the selection criteria a dataframe object of
    all selected games is returned.
    If no games meet the target, a message is displayed to advise and a 
    "No games" string is returned.
    """
    """
    number_of_games_back = How far back to go in comparing two teams
    difference_threshold_(home/away)win = How much difference is needed between
                                            teams to determine a win selection.
    difference_threshold_draw = How much difference between teams is too much 
                                for a draw.
    """
    
    method = ("WIN-DRAW - 1 - " + str(number_of_games_back) + " Games Back | " +
              "Home win goal dif better by >= " +
              str(difference_threshold_home_win) +
              " | away win goal dif better by >= " +
              str(difference_threshold_away_win) +
              " | draws with difference of <= " +
              str(difference_threshold_draw) + " | h/a specific")
    
    #Thresholds for selection
    """over_threshold_scored = 2
    over_threshold_conceded = 1
    under_threshold_scored = 0.5
    under_threshold_conceded = 1"""
    h_a_specific = True
    
    if h_a_specific:
        home = "home"
        away = "away"
    else:
        home = ""
        away = ""
    
    #Create a new dataframe for this data so that it can be exported.
    if not retrospective:
        win_df = pd.DataFrame(columns=["Method","Season","League Code","Date",
                                       "Time","HomeTeam","AwayTeam",
                                       "HomeScored","HomeConceded",
                                       "AwayScored","AwayConceded",
                                       "Difference","Prediction"])
    elif retrospective:
        win_df = pd.DataFrame(columns=["Method","Season","League Code","Date",
                                       "Time","HomeTeam","AwayTeam",
                                       "HomeScored","HomeConceded",
                                       "AwayScored","AwayConceded",
                                       "Difference","Prediction",
                                       "HomeTeam Score","AwayTeam Score",
                                       "Correct?"])
    current_row = 0
    

    for index, row in fixtures.iterrows():
        outcome = "Undecided"
        
        #Ensure the current fixture is in the selected leagues
        #(all fixtures are downloaded, so some fixtures may not belong to the
        #selected leagues)
        if (row["Div"] in list(c.leagues.values())):
            #Create a new fixture object if the fixture doesn't already exist.
            #(Multiple predictive functions can use the same fixture object).
            if ((row["Date"].strftime("%d/%m/%Y") + " - " + row["HomeTeam"] +
                 " - " + row["AwayTeam"]) not in c.fix_objs.keys()):
                c.fix_objs[row["Date"].strftime("%d/%m/%Y") + " - " + 
                           row["HomeTeam"] + " - " + row["AwayTeam"]] =(
                           Fixture(row["HomeTeam"],
                                   row["AwayTeam"],
                                   row["Date"],
                                   row["Time"]))
                
            #Check prior games (back from the date of the game - 1 day) for
            #comparative states
            from_date = row["Date"] - c.timedelta(days=1)
            
            home_conceded = c.team_objs[row["HomeTeam"]].get_goals_conceded_per_game(
                    h_a_specific=home, number_of_games=number_of_games_back,
                    seasons=[], from_date=from_date, to_date="")
            #get_goals_conceded_per_game may return "Not enough games available"
            if home_conceded == "Not enough games available":
                continue
            
            home_scored = c.team_objs[row["HomeTeam"]].get_goals_scored_per_game(
                    h_a_specific=home, number_of_games=number_of_games_back,
                    seasons=[], from_date=from_date, to_date="")
            #get_goals_scored_per_game may return "Not enough games available"
            if home_scored == "Not enough games available":
                continue
            
            away_conceded = c.team_objs[row["AwayTeam"]].get_goals_conceded_per_game(
                    h_a_specific=away, number_of_games=number_of_games_back,
                    seasons=[], from_date=from_date, to_date="")
            #get_goals_conceded_per_game may return "Not enough games available"
            if away_conceded == "Not enough games available":
                continue
            
            away_scored = c.team_objs[row["AwayTeam"]].get_goals_scored_per_game(
                    h_a_specific=away, number_of_games=number_of_games_back,
                    seasons=[], from_date=from_date, to_date="")
            #get_goals_scored_per_game may return "Not enough games available"
            if away_scored == "Not enough games available":
                continue
            
            difference = ((home_scored + away_conceded) -
                          (away_scored + home_conceded))
            
            if difference >= difference_threshold_home_win:
                outcome = "Home"
            
            if difference <= -difference_threshold_away_win:
                outcome = "Away"
                
            if (difference <= difference_threshold_draw and
                difference >= -difference_threshold_draw):
                outcome = "Draw"
             
            #Obtain season
            if retrospective:
                season = (c.merged_data.loc[c.merged_data["Date"] == row["Date"]]
                        ["Season"].iloc[0])
            elif not retrospective:
                season = (c.current_english_season[:2] + "-" + 
                          c.current_english_season[2:])
            
            if outcome != "Undecided" or show_all_games:
                if not retrospective:
                    new_row = (method,season,row["Div"],row["Date"],row["Time"],
                               row["HomeTeam"],row["AwayTeam"],home_scored,
                               home_conceded,away_scored,
                               away_conceded,difference,outcome)
                if retrospective:
                    if (
                            ((outcome=="Home") and (row["FTHG"]>row["FTAG"])) or
                            ((outcome=="Away") and (row["FTAG"]>row["FTHG"])) or
                            ((outcome=="Draw") and (row["FTAG"]==row["FTHG"]))):
                        correct = 1
                    else:
                        correct = 0
                    new_row = (method,season,row["Div"],row["Date"],row["Time"],
                               row["HomeTeam"],row["AwayTeam"],home_scored,
                               home_conceded,away_scored,
                               away_conceded,difference,outcome,row["FTHG"],
                               row["FTAG"],correct)
                #print(new_row)
                win_df.loc[current_row] = new_row
                current_row += 1
                
    if current_row == 0:
        print("\nNo suitable selections this time")
        return "No games"
    else:
        return  win_df

def generate_predictions(prediction_type, prediction_method):
    c.predictions_df = predictive_methods[prediction_type][prediction_method](
            c.fixtures)
    if type(c.predictions_df) == str:
            print("\nNo games were found that met the search requirements")
    else:
        c.predictions_df["Date"] = pd.to_datetime(c.predictions_df["Date"], dayfirst=True)
        
        date_range = (c.predictions_df["Date"].min().strftime("%d-%m-%Y") +
                      " - " + c.predictions_df["Date"].max().strftime("%d-%m-%Y"))
        
        predictions_file = (prediction_type + " - " + prediction_method 
                            + " - predictions - " + date_range + ".csv")
        if ((not os.path.exists(c.unprocessed_predictions_dir + predictions_file))
        and (not os.path.exists(c.old_preprocessed_predictions_dir + predictions_file))):
            print("Would you like to export this to a csv file?")
            ans = c.general_menu(["Yes","No"])
            if ans == "Yes":
                c.predictions_df.to_csv(c.unprocessed_predictions_dir +
                                        predictions_file)
                print("done")
        else:
            print("These predictions have already been saved.")
            print("They are in either the unprocessed_predictions or the preprocessed_predictions folder.\n")
    
predictive_methods = {"Win Draw":{"1": win_draw_1, "2": win_draw_2,
                                  "3": win_draw_3, "4": win_draw_4,
                                  "5": win_draw_5, "6": win_draw_6,
                                  "7": win_draw_7, "8": win_draw_8,
                                  "9": win_draw_9, "10": win_draw_10,
                                  "11": win_draw_11, "12": win_draw_12,
                                  "13": win_draw_13},
                    "Over Under 2.5 Goals":{"None":None}}