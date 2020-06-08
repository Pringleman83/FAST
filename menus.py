# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:34:03 2019

@author: david
"""
import common_functions as c
import predictive_functions2 as pf
#import pandas as pd
import prediction_analysis2 as pa
import os

def select_seasons(current_english_season, seasons):
    """
    Takes the current english season, and a list of seasons available.
    Returns a list of seasons selected.
    """
    print("\nSeason select")
    
    options = ["Load current season",
               "Load all seasons",
               "Load selected seasons",
               "Exit"]
    selection = c.general_menu(options)
    
    if selection == "Load current season":
        return [c.get_season_key(current_english_season)]
    elif selection == "Load all seasons":
        return list(seasons.keys())
    elif selection == "Load selected seasons":
        selected_seasons = c.multi_pick(list(seasons.keys()))
        """seasons_to_return = []
        for sel in selected_seasons:
            seasons_to_return.append(seasons[sel])
        return seasons_to_return"""
        return selected_seasons
    elif selection == "Exit":
        return "exit"

def main_menu():
    while True:
        print("\nMain Menu")
        selection = c.general_menu(["Display results",
                                    "Display fixtures",
                                    "Generate next game predictions",
                                    "Display predictions",
                                    "Prediction analysis options",
                                    "Back"])
        if selection == "Display results":
            display_results()
        elif selection == "Display fixtures":
            display_fixtures()
        elif selection == "Generate next game predictions":
            generate_predictions()
        elif selection == "Display predictions":
            display_predictions()
        elif selection == "Prediction analysis options":
            analysis()
        elif selection == "Back":
            return

def display_results():
    print("\n Display Results")
    selection = c.general_menu(["Last 1 game",
                               "Last x games",
                               "All results for current season",
                                "All resulst for defined seasons",
                                "Back"])
        
    if selection == "Last 1 game":
        results_last_1_game()
    elif selection == "Last x games":
        results_last_x_games()
    elif selection == "All results for current season":
        results_season()
    elif selection == "All results for defined seasons":
        results_defined_seasons()
    elif selection == "Back":
        return

def results_last_1_game():
    print("\nDisplay Results (1 Game)")
    print("\nSelect leagues")
    selection = c.multi_pick(list(c.leagues.keys()))
    c.display_results(leagues=selection)
    
def results_last_x_games():
    print("\nDisplay Results (x Games)")
    print("\nEnter number of past results to display")
    number = c.get_number()
    print("\nSelect leagues")
    selection = c.multi_pick(list(c.leagues.keys()))
    c.display_results(number_of_games=number, leagues=selection)
    
def results_season():
    print("\nDisplay results for this season")
    print("\nSelect leagues")
    selection = c.multi_pick(list(c.leagues.keys()))
    c.display_results(number_of_games=100, leagues=selection)
    
def results_defined_seasons():
    print("\nDisplay results for defined seasons")
    print("\nSelect seasons")
    seasons = c.multi_pick(c.seasons)
    print("\nSelect leagues")
    selection = c.multi_pick(list(c.leagues.keys()))
    c.display_results(number_of_games=20000, leagues=selection,
                      seasons = seasons)
    
def display_fixtures():
    print("\nDisplay Fixtures")
    selection = c.general_menu(["Display all upcoming fixtures",
                              "Display fixtures for specific teams",
                              "Back"])
    if selection == "Display all upcoming fixtures":
        print("\nDisplay all upcoming fixtures")
        c.display_fixtures()   
    elif selection == "Display fixtures for specific teams":
        print("\nDisplay fixtures for specific teams")
        print("\nSelect teams")
        teams = c.multi_pick(c.fixture_team_list)
        c.display_fixtures(teams=teams)
        return
    elif selection == "Back":
        return
    
def generate_predictions():
    print("\nGenerate Predictions")
    print("\nSelect a prediction type.")
    prediction_type = c.general_menu(list(pf.predictive_methods.keys()))
    print("\nSelect a predictive method.")
    prediction_methods = c.multi_pick(list(pf.predictive_methods[
            prediction_type].keys()),[])
    
    for prediction_method in prediction_methods:
        #TESTING DEBUG
        print("\nGenerating predictions for type: ", prediction_type,
              "method: ", prediction_method)
        #END OF TESTING DEBUG
        
        #Take the selected type and method and pass it to a function to run the
        #method and create a scv file.
        pf.generate_predictions(prediction_type, prediction_method)
    
def display_predictions():
    print("\nDisplay Predictions")

def analysis():
    print("\nPrediction Analysis Options")
    selection = c.general_menu(["Process prediction files",
                                "Test a predictive function",
                                "Review tested predictive methods"])
    if selection == "Process prediction files":
        files = []
        for a,b,filename in os.walk(c.unprocessed_predictions_dir):
            files.append(filename)
        
        if len(files)<1:
            print("There are no unprocessed prediction files")
        else:
            print("\nSelect files to process")
            selected_files = c.multi_pick(files[0], [])
            #files[0] is the list of files
            pa.process_prediction_files(selected_files)
            
    elif selection == "Test a predictive function":
        print("\nSelect a prediction type:")
        prediction_type = c.general_menu(list(pf.predictive_methods.keys()))
        print("\nSelect predictive methods:")
        prediction_methods = c.multi_pick(
                list(pf.predictive_methods[prediction_type].keys()), [])
        
        predictive_functions = []
        for prediction_method in prediction_methods:
            predictive_functions.append(
                    pf.predictive_methods[prediction_type][prediction_method])

        print("\nSelect leagues:")
        #Empty lists below for no selected items to prevent a bug where an item
        #from a previous list is somehow added to the selected items.
        leagues = c.multi_pick(list(c.leagues.keys()), []) 
        print("\nSelect seasons")
        
        #Only allow the selection of seasons where all leagues are available 
        available_seasons = []
        for season in list(c.loaded_seasons.keys()):
            if season in c.seasons_with_all_leagues:
                available_seasons.append(season)
        seasons = c.multi_pick(available_seasons, [])
        
        #Get list of league codes rather than names
        league_codes = []
        for l in leagues:
            league_codes.append(c.leagues[l])
        
        #Get list of season codes rather than names
        season_codes = []
        for s in seasons:
            season_codes.append(c.loaded_seasons[s])
        
        for predictive_function in predictive_functions:
            pa.win_draw_test_method(predictive_function, leagues = league_codes,
                               seasons = season_codes)

    elif selection == "Review tested predictive methods":
        pass
    