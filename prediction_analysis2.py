# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:37:48 2019

@author: david
"""
import common_functions as c
import pandas as pd
import os

def win_draw_test_method(method, leagues = list(c.leagues.values()),
                           seasons = list(c.seasons.values())):
    """
    WORK IN PROGRESS
    Takes a prediction method function.
    Optional list of leagues (league codes not names)
    Optional list of seasons (season codes, not names)
    Tests it over previous seasons for specified leagues.
    Saves reports of tests to a report for that method and an overall
    accumulative report.
    
    METHOD_TEST_ANALYSIS
    Every prediction for that method in a single spreadsheet.  

    METHOD TEST ACCURACY ANALYSIS
    Accuracy reports for:
        each league for each season   
        each season overall
        each league overall
        every game overall
    
    TYPE_TEST_ANALYSIS
    The stats for each method in a type.
        
    """
    
    """
    This function has a huge dictionary called grouped_accuracies.
    It holds total accuracy stats in grouped_accuracies["Total"]
    as a sub dictionary.
    It holds overall stats for each season in grouped_accuracies[season] as
    sub dictionaries.
    It holds overall stats for each league in each season in
    grouped_accuracies[season][league] as sub dictionaries.
    It holds overall stats for each league over all seasons in
    grouped_accuracies[league] as sub dictionaries.
    """
    #Create strings containing all leagues / all seasons passed to function.
    leagues_str = ""
    seasons_str = ""
    for league in leagues:
        if leagues_str == "":
            leagues_str += league
        else:
            leagues_str += ("+" + league)
    
    for season in seasons:
        if seasons_str == "":
            seasons_str += season
        else:
            seasons_str += ("+" + season)
            
    #Function variables
    #Get the prediction type and method
    pred_type, pred_method = c.get_pred_type_method_keys(method)
    print("\nTesting: ", pred_type, pred_method)
            
    #Prepare dataframes
    #Set up a dataframe for the current method
    method_test_analysis_df = pd.DataFrame(columns = [
            "Season","League Code", "Date", "Time", "HomeTeam", "AwayTeam",
            "Prediction", "HomeTeam Score", "AwayTeam Score", "Correct?"])
    
    method_test_accuracy_analysis_df = pd.DataFrame(columns=[
                        "Method", "Season", "League", "Number of Games",
                        "Number of Predictions", "Prediction Percentage",
                        "Overall Accuracy", "Number of Home Wins Predicted",
                        "Number of Accurate Home Wins",
                        "Home Win Accuracy",
                        "Number of Away Wins Predicted",
                        "Number of Accurate Away Wins",
                        "Away Win Accuracy",
                        "Number of Draws Predicted",
                        "Number of Accurate Draws",
                        "Draw Accuracy",
                        "Total Number of Wins Predicted",
                        "Total Number of Accurate Wins",
                        "Total Win Accuracy",
                        "Total Number Of Accurate Selections"])
    
    #Check if an analysis file exists for this predictive type
    if os.path.exists(c.method_test_analysis_dir + pred_type + ".csv"):       
        #Load it if it does
        type_test_accuracy_analytics_df = (
                pd.read_csv(c.method_test_analysis_dir + pred_type +
                            ".csv", usecols=
                            ["Method", "Season", "League", "Number of Games",
                            "Number of Predictions", "Prediction Percentage",
                            "Overall Accuracy",
                            "Number of Home Wins Predicted",
                            "Number of Accurate Home Wins",
                            "Home Win Accuracy",
                            "Number of Away Wins Predicted",
                            "Number of Accurate Away Wins",
                            "Away Win Accuracy",
                            "Number of Draws Predicted",
                            "Number of Accurate Draws",
                            "Draw Accuracy",
                            "Total Number of Wins Predicted",
                            "Total Number of Accurate Wins",
                            "Total Win Accuracy",
                            "Total Number Of Accurate Selections"]))
    else:
        #Create file
        type_test_accuracy_analytics_df = pd.DataFrame(columns=[
                            "Method", "Season", "League", "Number of Games",
                            "Number of Predictions", "Prediction Percentage",
                            "Overall Accuracy",
                            "Number of Home Wins Predicted",
                            "Number of Accurate Home Wins",
                            "Home Win Accuracy",
                            "Number of Away Wins Predicted",
                            "Number of Accurate Away Wins",
                            "Away Win Accuracy",
                            "Number of Draws Predicted",
                            "Number of Accurate Draws",
                            "Draw Accuracy",
                            "Total Number of Wins Predicted",
                            "Total Number of Accurate Wins",
                            "Total Win Accuracy",
                            "Total Number Of Accurate Selections"])

    """
    A dictionary holding each league and season which relates the
    leagues and seasons dictionaries (so it grows as more leagues 
    and seasons are added).
    Each league and season within this dictionary holds accumulative
    accuracy data for each league and season.
    At the end of testing, extra rows can be added to the dataframe
    for each league and then for each season and a row for overall
    accuracy figures.
    """
    grouped_accuracies = {}
    
    #Reset all_game counters
    all_game_home_win_predictions = 0
    all_game_accurate_home_wins = 0
    all_game_away_win_predictions = 0
    all_game_accurate_away_wins = 0
    all_game_draw_predictions = 0
    all_game_accurate_draws = 0
    all_game_undecided_games = 0
    
    for season in seasons:
        
        #Reset season counters
        season_home_win_predictions = 0
        season_accurate_home_wins = 0
        season_away_win_predictions = 0
        season_accurate_away_wins = 0
        season_draw_predictions = 0
        season_accurate_draws = 0
        season_undecided_games = 0
        
        grouped_accuracies[season] = {}
        
        print("Analysing season: ", season)
        for league in leagues:
            #Reset league counters
            league_home_win_predictions = 0
            league_accurate_home_wins = 0
            league_away_win_predictions = 0
            league_accurate_away_wins = 0
            league_draw_predictions = 0
            league_accurate_draws = 0
            league_undecided_games = 0
            
            if league not in grouped_accuracies:
                grouped_accuracies[league] = {}
                
            grouped_accuracies[season][league] = {}
            
            print("Analysing league: ", league)
            #Get the league-season results into a new dataframe
            #Each row is a fixture with results
            print("Setting results_df...")
            results_df = c.merged_data.loc[
                    (c.merged_data["Season"] == season) &
                    (c.merged_data["Div"] == league)]
            print("Done")
            
            #for index, row in results_df.iterrows():
            """
            Send the key fixture details of each game to the predictive function.
            """
            print("Getting predictions and results...")
            predictions_df = method(results_df, retrospective=True)
            print("Done")
            #Successfully generates predictions as the system would on the day.
            print("Counting stats...")
            for index,row in predictions_df.iterrows():
                if row["Prediction"] == "Home":
                    league_home_win_predictions += 1
                    season_home_win_predictions += 1
                    all_game_home_win_predictions += 1
                    if row["Correct?"] == 1:
                        league_accurate_home_wins += 1
                        season_accurate_home_wins += 1
                        all_game_accurate_home_wins += 1
                elif row["Prediction"] == "Away":
                    league_away_win_predictions += 1
                    season_away_win_predictions += 1
                    all_game_away_win_predictions += 1
                    if row["Correct?"] == 1:
                        league_accurate_away_wins += 1
                        season_accurate_away_wins += 1
                        all_game_accurate_away_wins += 1
                elif row["Prediction"] == "Draw":
                    league_draw_predictions += 1
                    season_draw_predictions += 1
                    all_game_draw_predictions += 1
                    if row["Correct?"] == 1:
                        league_accurate_draws += 1
                        season_accurate_draws += 1
                        all_game_accurate_draws += 1
                elif row["Prediction"] == "Undecided":
                    league_undecided_games += 1
                    season_undecided_games += 1
                    all_game_undecided_games += 1
            
            league_total_win_predictions = (league_home_win_predictions +
                                     league_away_win_predictions)
            
            league_total_accurate_wins = (league_accurate_home_wins +
                                   league_accurate_away_wins)
            
            league_total_predictions = (league_total_win_predictions +
                                        league_draw_predictions)
            
            league_total_games =(league_total_predictions +
                                 league_undecided_games)
            
            league_total_accurate = (league_total_accurate_wins +
                                     league_accurate_draws)
            
            if ((league_home_win_predictions == 0) or (
                    league_accurate_home_wins == 0)):
                league_home_win_accuracy = 0
            else:
                league_home_win_accuracy = (league_accurate_home_wins / 
                                     league_home_win_predictions) * 100
            
            if ((league_away_win_predictions == 0) or (
                    league_accurate_away_wins == 0)):
                league_away_win_accuracy = 0
            else:
                league_away_win_accuracy = (league_accurate_away_wins / 
                                     league_away_win_predictions) * 100     
                                     
            if ((league_draw_predictions == 0) or (
                    league_accurate_draws == 0)):
                league_draw_accuracy = 0
            else:
                league_draw_accuracy = (league_accurate_draws / 
                                     league_draw_predictions) * 100
                                 
            if ((league_total_win_predictions == 0) or (
                    league_total_accurate_wins == 0)):
                league_total_win_accuracy = 0
            else:
                league_total_win_accuracy = (league_total_accurate_wins / 
                                     league_total_win_predictions) * 100
            
            if ((league_total_predictions == 0) or (
                    league_total_accurate == 0)):
                league_total_accuracy = 0
            else:
                league_total_accuracy = (league_total_accurate / 
                                     league_total_predictions) * 100
                        
            grouped_accuracies[season][league]["Number of Games"] = (
                    league_total_games)
            
            grouped_accuracies[season][league]["Number of Predictions"] = (
                    league_total_predictions)
            
            grouped_accuracies[season][league]["Prediction Percentage"] = (
                    (league_total_predictions/league_total_games) * 100)
                
            grouped_accuracies[season][league]["Overall Accuracy"] = (
                    league_total_accuracy)
            
            grouped_accuracies[season][league]["Number of Home Wins Predicted"] = (
                    league_home_win_predictions)
            
            grouped_accuracies[season][league]["Number of Accurate Home Wins"] = (
                    league_accurate_home_wins)
            
            grouped_accuracies[season][league]["Home Win Accuracy"] = (
                    league_home_win_accuracy)
            
            grouped_accuracies[season][league]["Number of Away Wins Predicted"] = (
                    league_away_win_predictions)
            
            grouped_accuracies[season][league]["Number of Accurate Away Wins"] = (
                    league_accurate_away_wins)
            
            grouped_accuracies[season][league]["Away Win Accuracy"] = (
                    league_away_win_accuracy)
            
            grouped_accuracies[season][league]["Number of Draws Predicted"] = (
                    league_draw_predictions)
            
            grouped_accuracies[season][league]["Number of Accurate Draws"] = (
                    league_accurate_draws)
            
            grouped_accuracies[season][league]["Draw Accuracy"] = (
                    league_draw_accuracy)
            
            grouped_accuracies[season][league]["Total Number of Wins Predicted"] = (
                    league_total_win_predictions)

            grouped_accuracies[season][league]["Total Number of Accurate Wins"] = (
                    league_total_accurate_wins)
            
            grouped_accuracies[season][league]["Total Win Accuracy"] = (
                    league_total_win_accuracy)
            
            grouped_accuracies[season][league]["Total Number of Accurate Selections"] = (
                league_total_accurate_wins + league_accurate_draws)
            
            """
            Type
            
            The type_analysis stats should be counted.
            
            Then we go on to the next game in the list.
            
            Once the list is complete we add a row in the
            type_test_analysis and then go on to the next league.
            
            (Each season / league should have a separate row entry on the
            Type_test_analysis_df.)
            
            
            A combined for each season and a combined for each league could
            be held and added to a further df?
            
            Once all leagues and seasons are complete, the dataframes need
            to be saved to CSV files.
            
            Note - We don't need to know the method name before we create
            the df. A new df is created every time. We aren't updating an
            existing sheet.
            """     
            """
            #This saves all prediction spreadsheets for each game day
            predictions_df.to_csv(c.method_test_analysis_dir + pred_type + 
                                  "-" + pred_method + "-" + league + "-" +
                                  season + ".csv")"""
            
            #Add the predictions to the test analysis df
            method_test_analysis_df = (
                    method_test_analysis_df.append(predictions_df[[
            "Season","League Code", "Date", "Time", "HomeTeam", "AwayTeam",
            "Prediction", "HomeTeam Score", "AwayTeam Score", "Correct?"]]))
                
            #TODO
            
            
            #Update method_test_accuracy_analysis_df
            new_accuracy_row = (
                    pred_method, "Years: " + season, league,
                    grouped_accuracies[season][league]["Number of Games"],
                    grouped_accuracies[season][league]["Number of Predictions"],
                    grouped_accuracies[season][league]["Prediction Percentage"],
                    grouped_accuracies[season][league]["Overall Accuracy"],
                    grouped_accuracies[season][league]["Number of Home Wins Predicted"],
                    grouped_accuracies[season][league]["Number of Accurate Home Wins"],
                    grouped_accuracies[season][league]["Home Win Accuracy"],
                    grouped_accuracies[season][league]["Number of Away Wins Predicted"],
                    grouped_accuracies[season][league]["Number of Accurate Away Wins"],
                    grouped_accuracies[season][league]["Away Win Accuracy"],
                    grouped_accuracies[season][league]["Number of Draws Predicted"],
                    grouped_accuracies[season][league]["Number of Accurate Draws"],
                    grouped_accuracies[season][league]["Draw Accuracy"],
                    grouped_accuracies[season][league]["Total Number of Wins Predicted"],
                    grouped_accuracies[season][league]["Total Number of Accurate Wins"],
                    grouped_accuracies[season][league]["Total Win Accuracy"],
                    grouped_accuracies[season][league]["Total Number of Accurate Selections"])
            
            method_test_accuracy_analysis_df.loc[
            len(method_test_accuracy_analysis_df)] = new_accuracy_row
            
            #END OF LEAGUE
            
        #SET SEASON STATS
        
        season_total_win_predictions = (season_home_win_predictions +
                                     season_away_win_predictions)
        
        season_total_accurate_wins = (season_accurate_home_wins +
                                   season_accurate_away_wins)
            
        season_total_predictions = (season_total_win_predictions
                                    + season_draw_predictions)
        
        season_total_games = season_total_predictions + season_undecided_games
        
        season_total_accurate = (season_total_accurate_wins + 
                                 season_accurate_draws)
        
        if ((season_home_win_predictions == 0) or (
                season_accurate_home_wins == 0)):
            season_home_win_accuracy = 0
        else:
            season_home_win_accuracy = (season_accurate_home_wins / 
                                 season_home_win_predictions) * 100
        
        if ((season_away_win_predictions == 0) or (
                season_accurate_away_wins == 0)):
            season_away_win_accuracy = 0
        else:
            season_away_win_accuracy = (season_accurate_away_wins / 
                                 season_away_win_predictions) * 100     
                                 
        if ((season_draw_predictions == 0) or (season_accurate_draws == 0)):
            season_draw_accuracy = 0
        else:
            season_draw_accuracy = (season_accurate_draws / 
                                 season_draw_predictions) * 100
                             
        if ((season_total_win_predictions == 0) or (
                season_total_accurate_wins == 0)):
            season_total_win_accuracy = 0
        else:
            season_total_win_accuracy = (season_total_accurate_wins / 
                                 season_total_win_predictions) * 100
        
        if ((season_total_predictions == 0) or (season_total_accurate == 0)):
            season_total_accuracy = 0
        else:
            season_total_accuracy = (season_total_accurate / 
                                 season_total_predictions) * 100
        
        grouped_accuracies[season]["Number of Games"] = (
                season_total_games)
            
        grouped_accuracies[season]["Number of Predictions"] = (
                season_total_predictions)
        
        grouped_accuracies[season]["Prediction Percentage"] = (
                (season_total_predictions/season_total_games) * 100)
            
        grouped_accuracies[season]["Overall Accuracy"] = (
                season_total_accuracy)
        
        grouped_accuracies[season]["Number of Home Wins Predicted"] = (
                season_home_win_predictions)
        
        grouped_accuracies[season]["Number of Accurate Home Wins"] = (
                season_accurate_home_wins)
        
        grouped_accuracies[season]["Home Win Accuracy"] = (
                season_home_win_accuracy)
        
        grouped_accuracies[season]["Number of Away Wins Predicted"] = (
                season_away_win_predictions)
        
        grouped_accuracies[season]["Number of Accurate Away Wins"] = (
                season_accurate_away_wins)
        
        grouped_accuracies[season]["Away Win Accuracy"] = (
                season_away_win_accuracy)
        
        grouped_accuracies[season]["Number of Draws Predicted"] = (
                season_draw_predictions)
        
        grouped_accuracies[season]["Number of Accurate Draws"] = (
                season_accurate_draws)
        
        grouped_accuracies[season]["Draw Accuracy"] = season_draw_accuracy
        
        grouped_accuracies[season]["Total Number of Wins Predicted"] = (
                season_total_win_predictions)

        grouped_accuracies[season]["Total Number of Accurate Wins"] = (
                season_total_accurate_wins)
        
        grouped_accuracies[season]["Total Win Accuracy"] = (
                season_total_win_accuracy)
        
        grouped_accuracies[season]["Total Number of Accurate Selections"] = (
                season_total_accurate_wins + season_accurate_draws)
        
        new_accuracy_row = (
                    pred_method, "Years: " + season, leagues_str,
                    grouped_accuracies[season]["Number of Games"],
                    grouped_accuracies[season]["Number of Predictions"],
                    grouped_accuracies[season]["Prediction Percentage"],
                    grouped_accuracies[season]["Overall Accuracy"],
                    grouped_accuracies[season]["Number of Home Wins Predicted"],
                    grouped_accuracies[season]["Number of Accurate Home Wins"],
                    grouped_accuracies[season]["Home Win Accuracy"],
                    grouped_accuracies[season]["Number of Away Wins Predicted"],
                    grouped_accuracies[season]["Number of Accurate Away Wins"],
                    grouped_accuracies[season]["Away Win Accuracy"],
                    grouped_accuracies[season]["Number of Draws Predicted"],
                    grouped_accuracies[season]["Number of Accurate Draws"],
                    grouped_accuracies[season]["Draw Accuracy"],
                    grouped_accuracies[season]["Total Number of Wins Predicted"],
                    grouped_accuracies[season]["Total Number of Accurate Wins"],
                    grouped_accuracies[season]["Total Win Accuracy"],
                    grouped_accuracies[season]["Total Number of Accurate Selections"])
            
        method_test_accuracy_analysis_df.loc[
            len(method_test_accuracy_analysis_df)] = new_accuracy_row
            
        #END OF SEASON
        
    #Set all_game_stats
    all_game_total_win_predictions = (all_game_home_win_predictions +
                                     all_game_away_win_predictions)
    
    all_game_total_accurate_wins = (all_game_accurate_home_wins +
                                   all_game_accurate_away_wins)
            
    all_game_total_predictions = (all_game_total_win_predictions + 
                                  all_game_draw_predictions)
    
    all_game_total_games = (all_game_total_predictions +
                            all_game_undecided_games)
    
    all_game_total_accurate = (all_game_total_accurate_wins +
                               all_game_accurate_draws)
    
    if ((all_game_home_win_predictions == 0) or (
            all_game_accurate_home_wins == 0)):
        all_game_home_win_accuracy = 0
    else:
        all_game_home_win_accuracy = (all_game_accurate_home_wins / 
                             all_game_home_win_predictions) * 100
    
    if ((all_game_away_win_predictions == 0) or (
            all_game_accurate_away_wins == 0)):
        all_game_away_win_accuracy = 0
    else:
        all_game_away_win_accuracy = (all_game_accurate_away_wins / 
                             all_game_away_win_predictions) * 100     
                             
    if ((all_game_draw_predictions == 0) or (all_game_accurate_draws == 0)):
        all_game_draw_accuracy = 0
    else:
        all_game_draw_accuracy = (all_game_accurate_draws / 
                             all_game_draw_predictions) * 100
                         
    if ((all_game_total_win_predictions == 0) or (
            all_game_total_accurate_wins == 0)):
        all_game_total_win_accuracy = 0
    else:
        all_game_total_win_accuracy = (all_game_total_accurate_wins / 
                             all_game_total_win_predictions) * 100
    
    if ((all_game_total_predictions == 0) or (all_game_total_accurate == 0)):
        all_game_total_accuracy = 0
    else:
        all_game_total_accuracy = (all_game_total_accurate / 
                             all_game_total_predictions) * 100
                                   
    grouped_accuracies["Total"] = {}
    
    grouped_accuracies["Total"]["Number of Games"] = (
                    all_game_total_games)
            
    grouped_accuracies["Total"]["Number of Predictions"] = (
            all_game_total_predictions)
    
    if ((all_game_total_predictions == 0) or (all_game_total_games == 0)):
        grouped_accuracies["Total"]["Prediction Percentage"] = 0
    else:
        grouped_accuracies["Total"]["Prediction Percentage"] = (
                (all_game_total_predictions/all_game_total_games) * 100)
        
    grouped_accuracies["Total"]["Overall Accuracy"] = (
            all_game_total_accuracy)
    
    grouped_accuracies["Total"]["Number of Home Wins Predicted"] = (
            all_game_home_win_predictions)
    
    grouped_accuracies["Total"]["Number of Accurate Home Wins"] = (
            all_game_accurate_home_wins)
    
    grouped_accuracies["Total"]["Home Win Accuracy"] = (
            all_game_home_win_accuracy)
    
    grouped_accuracies["Total"]["Number of Away Wins Predicted"] = (
            all_game_away_win_predictions)
    
    grouped_accuracies["Total"]["Number of Accurate Away Wins"] = (
            all_game_accurate_away_wins)
    
    grouped_accuracies["Total"]["Away Win Accuracy"] = (
            all_game_away_win_accuracy)
    
    grouped_accuracies["Total"]["Number of Draws Predicted"] = (
            all_game_draw_predictions)
    
    grouped_accuracies["Total"]["Number of Accurate Draws"] = (
            all_game_accurate_draws)
    
    grouped_accuracies["Total"]["Draw Accuracy"] = all_game_draw_accuracy
    
    grouped_accuracies["Total"]["Total Number of Wins Predicted"] = (
            all_game_total_win_predictions)

    grouped_accuracies["Total"]["Total Number of Accurate Wins"] = (
            all_game_total_accurate_wins)
    
    grouped_accuracies["Total"]["Total Win Accuracy"] = (
            all_game_total_win_accuracy)
    
    grouped_accuracies["Total"]["Total Number of Accurate Selections"] = (
                all_game_total_accurate_wins + all_game_accurate_draws)
    
    #Set league stats for all seasons
    print("Calculating league totals...")
    
    #DEBUG
    """
    print()
    for x in grouped_accuracies.keys():
        print(x)
        print(grouped_accuracies[x])
        print()"""
    #END OF DEBUG
    
    for season in list(grouped_accuracies.keys()):
        #Ensure we're looking at a season (not "Total" or a league)
        if season not in seasons:
            continue
        for league in list(grouped_accuracies[season].keys()):
            #Ensure we're looking at a league and not overall seas stats
            if league not in leagues:
                continue
            if "Number of Games" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Games"] = (
                        grouped_accuracies[season][league]["Number of Games"])
            else:
                grouped_accuracies[league]["Number of Games"] += (
                        grouped_accuracies[season][league]["Number of Games"])
                
            if "Number of Predictions" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Predictions"] = (
                        grouped_accuracies[season][league]["Number of Predictions"])
            else:
                grouped_accuracies[league]["Number of Predictions"] += (
                        grouped_accuracies[season][league]["Number of Predictions"])
                
            if "Number of Home Wins Predicted" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Home Wins Predicted"] = (
                        grouped_accuracies[season][league]["Number of Home Wins Predicted"])
            else:
                grouped_accuracies[league]["Number of Home Wins Predicted"] += (
                        grouped_accuracies[season][league]["Number of Home Wins Predicted"])
    
            if "Number of Accurate Home Wins" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Accurate Home Wins"] = (
                        grouped_accuracies[season][league]["Number of Accurate Home Wins"])
            else:
                grouped_accuracies[league]["Number of Accurate Home Wins"] += (
                        grouped_accuracies[season][league]["Number of Accurate Home Wins"])
                
            if "Number of Away Wins Predicted" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Away Wins Predicted"] = (
                        grouped_accuracies[season][league]["Number of Away Wins Predicted"])
            else:
                grouped_accuracies[league]["Number of Away Wins Predicted"] += (
                        grouped_accuracies[season][league]["Number of Away Wins Predicted"])
                
            if "Number of Accurate Away Wins" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Accurate Away Wins"] = (
                        grouped_accuracies[season][league]["Number of Accurate Away Wins"])
            else:
                grouped_accuracies[league]["Number of Accurate Away Wins"] += (
                        grouped_accuracies[season][league]["Number of Accurate Away Wins"])
                
            if "Number of Draws Predicted" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Draws Predicted"] = (
                        grouped_accuracies[season][league]["Number of Draws Predicted"])
            else:
                grouped_accuracies[league]["Number of Draws Predicted"] += (
                        grouped_accuracies[season][league]["Number of Draws Predicted"])
                
            if "Number of Accurate Draws" not in grouped_accuracies[league]:
                grouped_accuracies[league]["Number of Accurate Draws"] = (
                        grouped_accuracies[season][league]["Number of Accurate Draws"])
            else:
                grouped_accuracies[league]["Number of Accurate Draws"] += (
                        grouped_accuracies[season][league]["Number of Accurate Draws"])
                
    
    #Calculate and add to DF the totals for each league over all seasons           
    for league in list(grouped_accuracies.keys()):
        #Ensure we're working with an actual league and not other data
        #DEBUG
        #print("League: ", league)
        #END OF DEBUG
        if league not in leagues:
            continue
        #DEBUG
        #print("League: ", league)
        #END OF DEBUG
        if ((grouped_accuracies[league]["Number of Predictions"] == 0) or
            (grouped_accuracies[league]["Number of Games"] == 0)):
            grouped_accuracies[league]["Prediction Percentage"] = 0
        else:
            grouped_accuracies[league]["Prediction Percentage"] = (
                            (grouped_accuracies[league]["Number of Predictions"] /
                             grouped_accuracies[league]["Number of Games"]) * 100)
        
        if ((grouped_accuracies[league]["Number of Accurate Home Wins"] == 0)
        or (grouped_accuracies[league]["Number of Home Wins Predicted"] == 0)):
            grouped_accuracies[league]["Home Win Accuracy"] = 0
        else:
            grouped_accuracies[league]["Home Win Accuracy"] = (
                    (grouped_accuracies[league]["Number of Accurate Home Wins"] /
                     grouped_accuracies[league]["Number of Home Wins Predicted"])
                     * 100)
                
        if ((grouped_accuracies[league]["Number of Accurate Away Wins"] == 0)
        or (grouped_accuracies[league]["Number of Accurate Away Wins"] == 0)):
            grouped_accuracies[league]["Away Win Accuracy"] = 0
        else:
            grouped_accuracies[league]["Away Win Accuracy"] = (
                    (grouped_accuracies[league]["Number of Accurate Away Wins"] /
                     grouped_accuracies[league]["Number of Away Wins Predicted"])
                     * 100)
        
        if ((grouped_accuracies[league]["Number of Accurate Draws"] == 0)
        or (grouped_accuracies[league]["Number of Draws Predicted"] == 0)):
            grouped_accuracies[league]["Draw Accuracy"] = 0
        else:
            grouped_accuracies[league]["Draw Accuracy"] = (
                    (grouped_accuracies[league]["Number of Accurate Draws"] /
                     grouped_accuracies[league]["Number of Draws Predicted"])
                     * 100)
        
        grouped_accuracies[league]["Total Number of Wins Predicted"] = (
                grouped_accuracies[league]["Number of Home Wins Predicted"] +
                grouped_accuracies[league]["Number of Away Wins Predicted"])
        
        grouped_accuracies[league]["Total Number of Accurate Wins"] = (
                grouped_accuracies[league]["Number of Accurate Home Wins"] +
                grouped_accuracies[league]["Number of Accurate Away Wins"])
        
        grouped_accuracies[league]["Total Number of Accurate Selections"] = (
                grouped_accuracies[league]["Total Number of Accurate Wins"] +
                grouped_accuracies[league]["Number of Accurate Draws"])
        
        if ((grouped_accuracies[league]["Total Number of Accurate Wins"] == 0)
        or (grouped_accuracies[league]["Total Number of Wins Predicted"] == 0)):
            grouped_accuracies[league]["Total Win Accuracy"] = 0
        else:
            grouped_accuracies[league]["Total Win Accuracy"] = (
                    (grouped_accuracies[league]["Total Number of Accurate Wins"] /
                     grouped_accuracies[league]["Total Number of Wins Predicted"])
                    * 100)
        if ((grouped_accuracies[league]["Total Number of Accurate Selections"] == 0)
        or (grouped_accuracies[league]["Number of Predictions"] == 0)):
            grouped_accuracies[league]["Overall Accuracy"] = 0
        else:
            grouped_accuracies[league]["Overall Accuracy"] = (
                    (grouped_accuracies[league]["Total Number of Accurate Selections"] /
                     grouped_accuracies[league]["Number of Predictions"])
                    * 100)
    
        new_accuracy_row = (
                    pred_method, seasons_str, league,
                    grouped_accuracies[league]["Number of Games"],
                    grouped_accuracies[league]["Number of Predictions"],
                    grouped_accuracies[league]["Prediction Percentage"],
                    grouped_accuracies[league]["Overall Accuracy"],
                    grouped_accuracies[league]["Number of Home Wins Predicted"],
                    grouped_accuracies[league]["Number of Accurate Home Wins"],
                    grouped_accuracies[league]["Home Win Accuracy"],
                    grouped_accuracies[league]["Number of Away Wins Predicted"],
                    grouped_accuracies[league]["Number of Accurate Away Wins"],
                    grouped_accuracies[league]["Away Win Accuracy"],
                    grouped_accuracies[league]["Number of Draws Predicted"],
                    grouped_accuracies[league]["Number of Accurate Draws"],
                    grouped_accuracies[league]["Draw Accuracy"],
                    grouped_accuracies[league]["Total Number of Wins Predicted"],
                    grouped_accuracies[league]["Total Number of Accurate Wins"],
                    grouped_accuracies[league]["Total Win Accuracy"],
                    grouped_accuracies[league]["Total Number of Accurate Selections"])
            
        method_test_accuracy_analysis_df.loc[
                len(method_test_accuracy_analysis_df)] = new_accuracy_row
    
    #Calculate and add to DF the totals for all leagues over all seasons
    new_accuracy_row = (
                    pred_method, seasons_str, leagues_str,
                    grouped_accuracies["Total"]["Number of Games"],
                    grouped_accuracies["Total"]["Number of Predictions"],
                    grouped_accuracies["Total"]["Prediction Percentage"],
                    grouped_accuracies["Total"]["Overall Accuracy"],
                    grouped_accuracies["Total"]["Number of Home Wins Predicted"],
                    grouped_accuracies["Total"]["Number of Accurate Home Wins"],
                    grouped_accuracies["Total"]["Home Win Accuracy"],
                    grouped_accuracies["Total"]["Number of Away Wins Predicted"],
                    grouped_accuracies["Total"]["Number of Accurate Away Wins"],
                    grouped_accuracies["Total"]["Away Win Accuracy"],
                    grouped_accuracies["Total"]["Number of Draws Predicted"],
                    grouped_accuracies["Total"]["Number of Accurate Draws"],
                    grouped_accuracies["Total"]["Draw Accuracy"],
                    grouped_accuracies["Total"]["Total Number of Wins Predicted"],
                    grouped_accuracies["Total"]["Total Number of Accurate Wins"],
                    grouped_accuracies["Total"]["Total Win Accuracy"],
                    grouped_accuracies["Total"]["Total Number of Accurate Selections"])
            
    method_test_accuracy_analysis_df.loc[
            len(method_test_accuracy_analysis_df)] = new_accuracy_row
    
    #Set a prelimanory file name for the accuracy report
    method_test_accuracy_filename = (c.method_test_analysis_dir +
                                     "Accuracy - " + pred_type + " - Method "
                                     + pred_method + ".csv")
    
    #If it already exists, add the current date and time
    if os.path.exists(method_test_accuracy_filename):
        method_test_accuracy_filename = (c.method_test_analysis_dir +
                                 "Accuracy - " + pred_type +
                                 " - Method " + pred_method + " - " +
                                 c.datetime.now().strftime("%d-%m-%Y-%H-%M") +
                                 ".csv")   
        
    #Save the method accuracy report using the above filename
    method_test_accuracy_analysis_df.to_csv(method_test_accuracy_filename,
                                            index=False)
    
    #Set a prelimanory file name fpr the method test file.
    method_test_analysis_filename = (c.method_test_analysis_dir +
                                     "Analysis - " + pred_type + " - Method " +
                                     pred_method + ".csv")
    
    #If the filename already exists add teh date and time to it
    if os.path.exists(method_test_analysis_filename):
        method_test_analysis_filename = (c.method_test_analysis_dir
                                 + "Analysis - " + pred_type +
                                 " - Method " + pred_method + " - " +
                                 c.datetime.now().strftime("%d-%m-%y-%H-%M") + 
                                 ".csv") 
        
    #Save the method test using the defined file nam
    method_test_analysis_df.to_csv(method_test_analysis_filename, index=False)
    
    type_test_accuracy_analytics_df = (
            type_test_accuracy_analytics_df.append(
                    method_test_accuracy_analysis_df))
    
    type_test_accuracy_analytics_df.to_csv(c.method_test_analysis_dir +
                                           pred_type + ".csv", index=False)
     #TODO Check if the type_test_accuracy_data as already in the DafaFrame
     #before adding 

def process_prediction_files(files):
    """
    Takes a list of prediction files (found in the unprocessed_predictions_dir).
    Processes each file by:
        Checking if all games have now played. Question if some have?
        If all played:
            *creates a new dataframe for predictions with results
            *adds the outcome and accurate? data to those columns.
            *creates / updates the collective analysis file for the predictive
            method.
            *creates / updates the collective analysis file for the predictive
            type.
            *saves the modified file to processed_predictions_dir.
            *moves the original file to old_preprocessed_predictions_dir.
    """
    #IN PROGRESS
    for file in files:
        #pred_type_analysis_exists = False#?
        #pred_method_analysis_exists = False#?
        
        #Load the original prediction file
        c.prediction_df = pd.read_csv(c.unprocessed_predictions_dir + file)
        
        #Determine the prediction type and method
        pred_type = (c.prediction_df["Method"][0].split(" - ")[0])
        pred_method = (c.prediction_df["Method"][0].split(" - ")[1])
        #print("Type", pred_type,"Method", pred_method)
        
        #Convert date column in original predictions to datetime objects
        c.prediction_df["Date"] = pd.to_datetime(
        c.prediction_df["Date"], dayfirst=True)
        
        #Establish the date range for file naming
        date_range = (c.prediction_df["Date"].min().strftime("%d-%m-%Y") 
        + " - " + c.prediction_df["Date"].max().strftime("%d-%m-%Y"))
        
        #Create a new dataframe so that we can add the scores and whether or
        #not the predictions were correct. This will ultimately be the csv
        #file that is saved in the processed predictions folder
        
        #Get columns from original predictions file (this is done because
        #different methods may have different columns)
        
        original_pred_cols = list(c.prediction_df)
        
        #New column list is original columns plus "HScore", "AScore" and "Correct"
        #[1:] gets rid of the "Unnamed: 0" column in original_pred_cols
        updated_pred_cols = original_pred_cols[1:] + ["HomeTeam Score",
                                                  "AwayTeam Score",
                                                  "Correct?"]
        
        #Create the updated dataframe with the new columns
        updated_prediction_df = pd.DataFrame(columns=updated_pred_cols)
        
        #Check if an analysis file exists for this predictive type
        if os.path.exists(c.accumulative_analysis_type_dir +
                          pred_type + ".csv"):       
            #Load it if it does
            type_analytics_df = (
                    pd.read_csv(c.accumulative_analysis_type_dir + pred_type +
                                ".csv", parse_dates = ["Date"]))
        else:
            #Create file
            type_analytics_df = pd.DataFrame(columns=["Method","Season",
                                                      "League Code","Date",
                                                      "Time","HomeTeam",
                                                      "AwayTeam","Prediction",
                                                      "HomeScore", "AwayScore",
                                                      "Correct?"])
            
        #Check if an analysis file exists for this method
        if os.path.exists(c.accumulative_analysis_method_dir 
                          + pred_type + " method " + pred_method + ".csv"):
            method_analytics_df = (
                    pd.read_csv(c.accumulative_analysis_method_dir + pred_type
                                + " method " + pred_method + ".csv",
                                parse_dates = ["Date"]))
        else:
            #Create file
            method_analytics_df = pd.DataFrame(columns=updated_pred_cols)
        
        #Check if an accuracy_analysis file exists
        if os.path.exists(c.accuracy_analysis_dir + pred_type +
                                         " accuracy_analytics.csv"):
            #Includes specified columns to avoid errors caused by unexpected
            #blank columns (possibly as a result of editing outside of the 
            #script)
            accuracy_analytics_df = (
                    pd.read_csv(c.accuracy_analysis_dir + pred_type +
                                " accuracy_analytics.csv", usecols=
                                ['Date Range', 'Method', 'Number of Games',
                                 'Number of Predictions',
                                 'Prediction Percentage',
                                 'Overall Accuracy',
                                 'Number of Home Wins Predicted',
                                 'Number of Accurate Home Wins',
                                 'Home Win Accuracy',
                                 'Number of Away Wins Predicted',
                                 'Number of Accurate Away Wins',
                                 'Away Win Accuracy',
                                 'Number of Draws Predicted',
                                 'Number of Accurate Draws',
                                 'Draw Accuracy',
                                 'Total Number of Wins Predicted',
                                 'Total Number of Accurate Wins',
                                 'Total Win Accuracy']))

        else:
            #Create file
            if pred_type == "WIN-DRAW":
                accuracy_analytics_df = pd.DataFrame(columns=[
                        "Date Range", "Method", "Number of Games",
                        "Number of Predictions", "Prediction Percentage",
                        "Overall Accuracy", "Number of Home Wins Predicted",
                        "Number of Accurate Home Wins",
                        "Home Win Accuracy",
                        "Number of Away Wins Predicted",
                        "Number of Accurate Away Wins",
                        "Away Win Accuracy",
                        "Number of Draws Predicted",
                        "Number of Accurate Draws",
                        "Draw Accuracy",
                        "Total Number of Wins Predicted",
                        "Total Number of Accurate Wins",
                        "Total Win Accuracy"])
            elif pred_type == "OVER UNDER 2.5":
                #TODO Set this up for over 2.5 goals.
                accuracy_analytics_df = pd.DataFrame(columns=[
                        "Date Range", "Method", "Number of Games",
                        "Number of Predictions", "Prediction Percentage",
                        "Overall Accuracy", "Number of Home Wins Predicted",
                        "Number of Accurate Home Wins",
                        "Home Win Accuracy",
                        "Number of Away Wins Predicted",
                        "Number of Accurate Away Wins",
                        "Away Win Accuracy",
                        "Number of Draws Predicted",
                        "Number of Accurate Draws",
                        "Draw Accuracy",
                        "Total Number of Wins Predicted",
                        "Total Number of Accurate Wins",
                        "Total Win Accuracy"])
        
        number_of_games = len(c.prediction_df.index)
        correct_results = 0
        correct_home_wins = 0
        correct_away_wins = 0
        correct_wins = 0
        correct_draws = 0
        games_not_found = 0
        
        undecided_games = len(c.prediction_df.loc[
                c.prediction_df["Prediction"] == "Undecided"])
        
        number_of_selections = number_of_games - undecided_games
        
        home_win_predictions = len(c.prediction_df.loc[
                c.prediction_df["Prediction"] == "Home"])

        away_win_predictions = len(c.prediction_df.loc[
                c.prediction_df["Prediction"] == "Away"])
        
        draw_predictions = len(c.prediction_df.loc[
                c.prediction_df["Prediction"] == "Draw"])
        
        total_win_predictions = home_win_predictions + away_win_predictions
        
        total_predictions = total_win_predictions + draw_predictions
        
        total_games = total_predictions + undecided_games
        
        #DEBUG (May keep)
        if total_games == number_of_games:
            print ("Self test pass - Total predictions matches number of games")
            if undecided_games:
                print (str(undecided_games) + " games were too close to call" +
                       " and are therefore undecided")
        else:
            print ("Self test fail! - Total games on prediction sheet = " +
                   str(total_predictions) + " number_of_games = " +
                   str(number_of_games))
        #END OF DEBUG
        
        method = ""
        
        for index, row in c.prediction_df.iterrows():
            #For each prediction find the matching result in the merged data
            #collection of game results
            result_record = c.merged_data.loc[((c.merged_data["Date"] == row["Date"])
            & (c.merged_data["Div"] == row["League Code"]) )
            & ( (c.merged_data["HomeTeam"] == row["HomeTeam"])
            & (c.merged_data["AwayTeam"] == row["AwayTeam"]) )]
            
            #DEBUG
            #print(record)
            #input()
            
            #If no prediciton method has yet been determined, set it as what
            #is in the current row
            if not method:
                method = row["Method"]
            
            #If no matching result has been found store it as a no result
            if result_record.empty:
                print("Result not found: " + row["League Code"],row["Date"],
                      row["Time"],row["HomeTeam"],row["AwayTeam"])
                games_not_found += 1
                new_updated_prediction_row = [method,row["Season"],
                                              row["League Code"],row["Date"],
                                              row["Time"],row["HomeTeam"],
                                              row["AwayTeam"],
                                              row["HomeScored"],
                                              row["HomeConceded"],
                                              row["AwayScored"],
                                              row["AwayConceded"],
                                              row["Prediction"],
                                              "NO RESULT","NO RESULT", 0]
                
            #If a result is found, get the scores, determine if correct and
            #count stats
            else:

                if (row["Prediction"] == "Home" and 
                    int(result_record["FTHG"]) > int(result_record["FTAG"])): 
                    correct = 1
                elif (row["Prediction"] == "Away" and
                      int(result_record["FTAG"]) > int(result_record["FTHG"])):
                    correct = 1
                elif (row["Prediction"] == "Draw" and 
                      int(result_record["FTHG"]) == int(result_record["FTAG"])):
                    correct = 1
                else:
                    correct = 0
                
                new_updated_prediction_row = [method,row["Season"],
                                              row["League Code"],
                                              row["Date"],row["Time"],
                                              row["HomeTeam"],
                                              row["AwayTeam"],
                                              row["HomeScored"],
                                              row["HomeConceded"],
                                              row["AwayScored"],
                                              row["AwayConceded"],
                                              row["Difference"],
                                              row["Prediction"],
                                              int(result_record["FTHG"]),
                                              int(result_record["FTAG"]),
                                              correct]
                
                new_type_analysis_row = [method,row["Season"],
                                         row["League Code"],
                                         row["Date"],row["Time"],
                                         row["HomeTeam"],
                                         row["AwayTeam"],
                                         row["Prediction"],
                                         int(result_record["FTHG"]),
                                         int(result_record["FTAG"]),
                                         correct]
                
                #NO NEED TO CREATE A METHOD ANALYSIS ROW AS IT'S THE
                #SAME AS THE UPDATED PREDICTION ROW
                
                #Add the new prediction row to the new prediction dataframe
                #and to the method analysis dataframe
                updated_prediction_df.loc[len(updated_prediction_df)] = (
                        new_updated_prediction_row)
                
                #Check if row already exists in method_analytics_df
                #If not, add it to that and the type_analytics_df
                duplicate = False
                for index, row in method_analytics_df.iterrows():
                    if ((row["Date"] == new_updated_prediction_row[2]) and
                        (row["HomeTeam"] == new_updated_prediction_row[3]) and
                        (row["AwayTeam"] == new_updated_prediction_row[4]) and
                        (row["FTHG"] == new_updated_prediction_row[11]) and
                        (row["FTAG"] == new_updated_prediction_row[12])):
                        print(row["Date"],row["HomeTeam"],row["AwayTeam"],
                                  "already in method analytics sheet. ",
                                  "Not added this time.")
                        duplicate = True
                        break
                    
                #REMINDER - We have separate method and type spreadsheets
                #because different methods may provide different data.
                #The type spreadsheet doesn't hold this data.
                #The individual method one does.
                if not duplicate:
                    #Add to method_analytics_df
                    method_analytics_df.loc[len(method_analytics_df)] = (
                            new_updated_prediction_row)
                    #Add to type_analyitics dataframe
                    type_analytics_df.loc[len(type_analytics_df)] = (
                            new_type_analysis_row)

                #Count correct predictions
                #Home wins and wins
                if correct and (int(result_record["FTHG"]) >
                                int(result_record["FTAG"])):
                    correct_home_wins += 1
                    correct_wins += 1
                    correct_results += 1
                
                #Away wins and wins
                if correct and (int(result_record["FTAG"]) >
                                int(result_record["FTHG"])):
                    correct_away_wins += 1
                    correct_wins += 1
                    correct_results += 1
                    
                #Draws
                if correct and (int(result_record["FTHG"]) ==
                                int(result_record["FTAG"])):
                    correct_draws += 1
                    correct_results += 1
        
        if games_not_found > 0:
            print(str(games_not_found) +
                  " games not found. Continue with results analysis?")
            cont = c.general_menu(["Yes","No"])
            if cont == "No":
                return 0
        
        if correct_results == 0 or number_of_selections == 0:
            total_accuracy = 0
        else:
            total_accuracy = (correct_results / number_of_selections) * 100
        
        if total_win_predictions == 0 or correct_wins == 0:
            total_win_accuracy = 0
        else:
            total_win_accuracy = (correct_wins / total_win_predictions) * 100
        
        if draw_predictions == 0 or correct_draws == 0:
            total_draw_accuracy = 0
        else:
            total_draw_accuracy = (correct_draws / draw_predictions) * 100
            
        if home_win_predictions == 0 or correct_home_wins == 0:
            home_win_accuracy = 0
        else:
            home_win_accuracy = (correct_home_wins / home_win_predictions) * 100
            
        if away_win_predictions == 0 or correct_away_wins == 0:
            away_win_accuracy = 0
        else:
            away_win_accuracy = (correct_away_wins / away_win_predictions) * 100
        
        if total_predictions == 0:
            prediction_percentage = 0
        else:
            prediction_percentage = (total_predictions/total_games) * 100
        
        if pred_type == "WIN-DRAW":
            new_analytics_row = [date_range, method, number_of_games,
                                 total_predictions, prediction_percentage,
                                 total_accuracy, home_win_predictions,
                                 correct_home_wins, home_win_accuracy,
                                 away_win_predictions, correct_away_wins,
                                 away_win_accuracy, draw_predictions,
                                 correct_draws, total_draw_accuracy,
                                 total_win_predictions, correct_wins,
                                 total_win_accuracy]
        elif pred_type == "OVER UNDER 2.5":
            #NEEDS TO BE CORRECTED FOR THIS TYPE
            #TODO
            new_analytics_row = [date_range, method, number_of_games,
                                 total_predictions, prediction_percentage,
                                 total_accuracy, home_win_predictions,
                                 correct_home_wins, home_win_accuracy,
                                 away_win_predictions, correct_away_wins,
                                 away_win_accuracy, draw_predictions,
                                 correct_draws, total_draw_accuracy,
                                 total_win_predictions, correct_wins,
                                 total_win_accuracy]
        
        #Add the new row to the accuracy_analytics_df
        accuracy_analytics_df.loc[len(accuracy_analytics_df)] = (
                new_analytics_row)
        
        #Correct the index now that the new row has been added
        accuracy_analytics_df.reset_index()           
        
        #Save the updated predictions file with outcomes to the processed_
        #predictions folder
        updated_prediction_df.to_csv(c.processed_predictions_dir+ method[:12] +
                                     " - results - " + date_range + ".csv")
        
        #Move the original prediction file to the original files folder.
        os.rename(c.unprocessed_predictions_dir + file,
                  c.old_preprocessed_predictions_dir + file)
        
        #Save the accumulative_method_analytics file to the relevant folder
        method_analytics_df.to_csv(c.accumulative_analysis_method_dir 
                          + pred_type + " method " + pred_method + ".csv",
                                   index=False)
        
        #Save the accumulative_type_analytics file to the relevant folder
        type_analytics_df.to_csv(c.accumulative_analysis_type_dir
                                             + pred_type + ".csv", index=False)
    
        #Save the updated general accuracy_analytics file to the relevant
        #folder
        #(Do this for all types anyway?)if pred_type == "WIN-DRAW":
        accuracy_analytics_df.to_csv(c.accuracy_analysis_dir + pred_type +
                                     " accuracy_analytics.csv", index=False)
    print("\nDone")