# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:44:12 2019

@author: david
"""
import common_functions as c

#Classes

class Team(object):
    #class variables
    teams = []
    def __init__ (self, name):
        #Add object to Class.teams list.
        self.teams.append(self)
        
        #A dictionoary for storing values that are gathered using methods
        #to save the same method having to run again.
        self.fetched_values = {"home goals scored":{},"away goals scored":{},
                               "total goals scored":{},"home games played":{},
                               "away games played":{},"total games played":{},
                               "home goals conceded":{},"away goals conceded":{},
                               "total goals conceded":{},
                               "home goals scored and conceded":{},
                               "away goals scored and conceded":{},
                               "total goals scored and conceded":{},
                               "home goals scored and conceded pg":{},
                               "away goals scored and conceded pg":{},
                               "total goals scored and conceded pg":{},
                               "home goal difference":{},
                               "home goal difference pg":{},
                               "away goal difference":{},
                               "away goal difference pg":{},
                               "total goal difference":{},
                               "total goal difference pg":{},
                               "home wins":{},"away wins":{},"total wins":{},
                               "home losses":{},"away losses":{},"total losses":{},
                               "home draws":{},"away draws":{},"total draws":{},
                               "home points":{},"away points":{},"total points":{},
                               "home wins pg":{},"away wins pg":{},"total wins pg":{},
                               "home losses pg":{},"away losses pg":{},
                               "total losses pg":{},"home draws pg":{},
                               "away draws pg":{},"total draws pg":{},
                               "home goals scored pg":{},"away goals scored pg":{},
                               "total goals scored pg":{},"home goals conceded pg":{},
                               "away goals conceded pg":{},"total goals conceded pg":{},
                               "home played":{},"away played":{},"total played":{},
                               "home points pg":{},"away points pg":{},"total points pg":{}}
        
        #Basic instance variables
        self.team_name = name   
        self.league = c.get_latest_league(self.team_name)
    
    
    def get_results(self, from_date=c.now, to_date="", number_of_games = 100,
                    h_a_specific=False, season=""):
        """
        Takes optional values:
            from_date (datetime object for the start of the time we want to go back from)
            to_date (datetime object determining how far to go back)
            number_of_games (number of games to go back)
            h_a_specific (False, "home" or "away" to select what games are returned.)
        Returns a dataframe of the requested games.
        """
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date
            to_date = from_date-c.timedelta(days=20000)
            
        if not season:
            #If no season specified, use dates specified
            new_df=c.merged_data[((c.merged_data["HomeTeam"] == self.team_name) | 
                    (c.merged_data["AwayTeam"] == self.team_name)) & (
                            (c.merged_data["Date"] < from_date) & 
                            (c.merged_data["Date"] > to_date))]
        else:
            #If season is specified, ensure that only tha seasons games are used
            new_df=c.merged_data[((c.merged_data["HomeTeam"] == self.team_name) | 
                    (c.merged_data["AwayTeam"] == self.team_name)) & (
                            (c.merged_data["Date"] < from_date) & 
                            (c.merged_data["Date"] > to_date)) &
                            (c.merged_data["Season"] == season)]  
    
        if not h_a_specific:
            if len(new_df.loc[((new_df["HomeTeam"] == self.team_name)
                | (new_df["AwayTeam"] == self.team.name))]) < number_of_games:
                return "Not enough games available"
            else:
                return new_df.head(number_of_games)
        if h_a_specific.lower() == "home":
            if len(new_df.loc[new_df["HomeTeam"] == self.team_name]) < number_of_games:
                return "Not enough games available"
            else:
                return new_df[(new_df["HomeTeam"] == self.team_name)].head(number_of_games)
        if h_a_specific.lower() == "away":
            if len(new_df.loc[new_df["AwayTeam"] == self.team_name]) < number_of_games:
                return "Not enough games available"
            else:
                return new_df[(new_df["AwayTeam"] == self.team_name)].head(number_of_games)
        
    def get_goals_scored(self, h_a_specific="", number_of_games=0, seasons=[],
                         from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns goals scored for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set of goals
        scored.
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games, seasons):
            print("#####")
            print("get_goals_scored: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals scored"
        elif h_a_specific.lower() == "home":
            stat = "home goals scored"
        elif h_a_specific.lower() == "away":
            stat = "away goals scored"
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " + 
                    to_date.strftime("%d%m%y") + " " + str(number_of_games)
                    + " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "", 
                                      from_date = from_date, 
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored = (df.loc[(df["HomeTeam"] == self.team_name)]["FTHG"].sum() 
                + df.loc[(df["AwayTeam"] == self.team_name)]["FTAG"].sum())
                self.fetched_values[stat][stat_key] = goals_scored
                return goals_scored
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored = df["FTHG"].sum()
                self.fetched_values[stat][stat_key] = goals_scored
                return goals_scored
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored = df["FTAG"].sum()
                self.fetched_values[stat][stat_key] = goals_scored
                return goals_scored
            
    def get_goals_conceded(self, h_a_specific="", number_of_games=0,
                           seasons=[], from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns goals conceded for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set of goals
        conceded.
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games, seasons):
            print("#####")
            print("get_goals_conceded: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals conceded"
        elif h_a_specific.lower() == "home":
            stat = "home goals conceded"
        elif h_a_specific.lower() == "away":
            stat = "away goals conceded"
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " + 
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_conceded = (df.loc[(df["HomeTeam"] == self.team_name)]["FTAG"].sum()
                                + df.loc[(df["AwayTeam"] == self.team_name)]["FTHG"].sum())
                self.fetched_values[stat][stat_key] = goals_conceded
                return goals_conceded
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_conceded = df["FTAG"].sum()
                self.fetched_values[stat][stat_key] = goals_conceded
                return goals_conceded
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_conceded = df["FTHG"].sum()
                self.fetched_values[stat][stat_key] = goals_conceded
                return goals_conceded
        
    def get_goals_scored_conceded(self, h_a_specific = "",
                                  number_of_games=0, seasons=[],
                                  from_date=c.now, to_date=""):
        """
        Takes optional h_a_specific string,
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns goals scored and conceded for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set of goals
        scored and conceded.
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_goals_scored_conceded: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals scored and conceded"
        elif h_a_specific.lower() == "home":
            stat = "home goals scored and conceded"
        elif h_a_specific.lower() == "away":
            stat = "away goals scored and conceded"
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " + 
                    to_date.strftime("%d%m%y") + " " + 
                    str(number_of_games) + " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored_conceded = df["FTAG"].sum() + df["FTHG"].sum()
                self.fetched_values[stat][stat_key] = goals_scored_conceded
                return goals_scored_conceded
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored_conceded = df["FTAG"].sum() + df["FTHG"].sum()
                self.fetched_values[stat][stat_key] = goals_scored_conceded
                return goals_scored_conceded
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                goals_scored_conceded = df["FTAG"].sum() + df["FTHG"].sum()
                self.fetched_values[stat][stat_key] = goals_scored_conceded
                return goals_scored_conceded
    
    def get_win_count(self, h_a_specific="", number_of_games=0, seasons=[],
                      from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns the number of wins for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set wins
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_win_count: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total wins"
        elif h_a_specific.lower() == "home":
            stat = "home wins"
        elif h_a_specific.lower() == "away":
            stat = "away wins"
        
        win_count = 0
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                for index, row in df.iterrows():
                    if row["HomeTeam"] == self.team_name and row["FTHG"] > row["FTAG"]:
                        win_count += 1
                    elif row["AwayTeam"] == self.team_name and row["FTAG"] > row["FTHG"]:
                        win_count += 1
                self.fetched_values[stat][stat_key] = win_count
                return win_count
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                for index, row in df.iterrows():
                    if row["FTHG"] > row["FTAG"]:
                            win_count += 1
                self.fetched_values[stat][stat_key] = win_count
                return win_count
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                
                for index, row in df.iterrows():
                    if row["FTAG"] > row["FTHG"]:
                            win_count += 1
                self.fetched_values[stat][stat_key] = win_count
                return win_count
            
    def get_loss_count(self, h_a_specific="", number_of_games=0, seasons=[],
                       from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns the number of losses for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set's losses
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_loss_count: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total losses"
        elif h_a_specific.lower() == "home":
            stat = "home losses"
        elif h_a_specific.lower() == "away":
            stat = "away losses"
        
        loss_count = 0
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["HomeTeam"] == self.team_name and row["FTHG"] < row["FTAG"]:
                        loss_count += 1
                    elif row["AwayTeam"] == self.team_name and row["FTAG"] < row["FTHG"]:
                        loss_count += 1
                self.fetched_values[stat][stat_key] = loss_count
                return loss_count
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["FTHG"] < row["FTAG"]:
                            loss_count += 1
                self.fetched_values[stat][stat_key] = loss_count
                return loss_count
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["FTAG"] < row["FTHG"]:
                            loss_count += 1
                self.fetched_values[stat][stat_key] = loss_count
                return loss_count
            
    def get_draw_count(self, h_a_specific="", number_of_games=0, seasons=[],
                       from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns the number of draws for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that set's draws
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_draw_count: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total draws"
        elif h_a_specific.lower() == "home":
            stat = "home draws"
        elif h_a_specific.lower() == "away":
            stat = "away draws"
        
        draw_count = 0
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            if not h_a_specific:
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["FTHG"] == row["FTAG"]:
                        draw_count += 1
                self.fetched_values[stat][stat_key] = draw_count
                return draw_count
            
            if h_a_specific.lower() == "home":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "home",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["FTHG"] == row["FTAG"]:
                            draw_count += 1
                self.fetched_values[stat][stat_key] = draw_count
                return draw_count
            
            if h_a_specific.lower() == "away":
                df = self.get_results(number_of_games = number_of_games,
                                      h_a_specific = "away",
                                      from_date = from_date,
                                      to_date = to_date)
                #Get results may return "Not enough games available"
                if type(df) == str:
                    return df
                for index, row in df.iterrows():
                    if row["FTAG"] == row["FTHG"]:
                            draw_count += 1
                self.fetched_values[stat][stat_key] = draw_count
                return draw_count
        
    def get_avg_wins_per_game(self, h_a_specific="", number_of_games=0,
                              seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_wins_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total wins pg"
        elif h_a_specific.lower() == "home":
            stat = "home wins pg"
        elif h_a_specific.lower() == "away":
            stat = "away wins pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            win_count = self.get_win_count(h_a_specific=h_a_specific,
                                           number_of_games=number_of_games,
                                           from_date=from_date,
                                           to_date=to_date)
            #get_win_count may return "Not enough games available"
            if type(win_count) == str:
                return win_count
            if win_count == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = win_count / number_of_games
                return win_count / number_of_games
            
    def get_avg_losses_per_game(self, h_a_specific="", number_of_games=0,
                                seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_losses_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total losses pg"
        elif h_a_specific.lower() == "home":
            stat = "home losses pg"
        elif h_a_specific.lower() == "away":
            stat = "away losses pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            loss_count = self.get_loss_count(h_a_specific=h_a_specific,
                                             number_of_games=number_of_games,
                                             from_date=from_date,
                                             to_date=to_date)
            
            #get_loss_count may return "Not enough games available"
            if type(loss_count) == str:
                return loss_count
            
            if loss_count == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = loss_count / number_of_games
                return loss_count / number_of_games
    
    def get_avg_draws_per_game(self, h_a_specific="", number_of_games=0,
                               seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_draws_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total draws pg"
        elif h_a_specific.lower() == "home":
            stat = "home draws pg"
        elif h_a_specific.lower() == "away":
            stat = "away draws pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            draw_count = self.get_draw_count(h_a_specific=h_a_specific,
                                             number_of_games=number_of_games,
                                             from_date=from_date,
                                             to_date=to_date)
            
            #get_draw_count may return "Not enough games available"
            if type(draw_count) == str:
                return draw_count
            
            if draw_count == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = draw_count / number_of_games
                return draw_count / number_of_games
    
    def get_goals_scored_per_game(self, h_a_specific="", number_of_games=0,
                                  seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_goals_scored_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals scored pg"
        elif h_a_specific.lower() == "home":
            stat = "home goals scored pg"
        elif h_a_specific.lower() == "away":
            stat = "away goals scored pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            goals_scored = self.get_goals_scored(h_a_specific=h_a_specific,
                                                 number_of_games=number_of_games,
                                                 from_date=from_date,
                                                 to_date=to_date)
            
            #get_goals_scored may return "Not enough games available"
            if type(goals_scored) == str:
                return goals_scored
            if goals_scored == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = goals_scored / number_of_games
                return goals_scored / number_of_games
    
    def get_goals_conceded_per_game(self, h_a_specific="", number_of_games=0,
                                    seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_goals_conceded_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals conceded pg"
        elif h_a_specific.lower() == "home":
            stat = "home goals conceded pg"
        elif h_a_specific.lower() == "away":
            stat = "away goals conceded pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " +
                    str(number_of_games) + " games")
        
        if number_of_games:
            goals_conceded = self.get_goals_conceded(h_a_specific=h_a_specific,
                                                     number_of_games=number_of_games,
                                                     from_date=from_date,
                                                     to_date=to_date)
            #get_goals_conceded may return "Not enough games available"
            if type(goals_conceded) == str:
                return goals_conceded
            if goals_conceded == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = goals_conceded / number_of_games
                return goals_conceded / number_of_games
    
    def get_goals_scored_conceded_per_game(self, h_a_specific="",
                                           number_of_games=0, seasons=[],
                                           from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_avg_goals_conceded_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goals scored and conceded pg"
        elif h_a_specific.lower() == "home":
            stat = "home goals scored and conceded pg"
        elif h_a_specific.lower() == "away":
            stat = "away goals scored and conceded pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            goals_scored_conceded = self.get_goals_scored_conceded(h_a_specific=h_a_specific,
                                                                   number_of_games=number_of_games,
                                                                   from_date=from_date,
                                                                   to_date=to_date)
            #get_goals_scored_conceded may return "Not enough games available"
            if type(goals_scored_conceded) == str:
                return goals_scored_conceded
            if goals_scored_conceded == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = goals_scored_conceded / number_of_games
                return goals_scored_conceded / number_of_games
            
    def get_goal_difference(self, h_a_specific="", number_of_games=0,
                            seasons=[], from_date=c.now, to_date=""):
        """
        Takes optional inputs of h_a_specific(string),
        no_of_games(int),
        seasons(list),
        date_from(datetime object)
        
        Checks if the request has already been made and is stored. If so,
        returns the request.
        If not, carries out the request.
        
        If h_a_specific is False (as default), returns goal difference for the
        no_of_games or for the seasons listed prior to the date_from (not
        inclusive).
        
        If h_a_specific is "home" or is "away" returns only that goal difference.
        
        When a figure is returned, it's also stored to speed up future requests.
        """
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_goal_difference: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goal difference"
        elif h_a_specific.lower() == "home":
            stat = "home goal difference"
        elif h_a_specific.lower() == "away":
            stat = "away goal difference"
        
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        if number_of_games:
            if stat_key in self.fetched_values[stat]:
                return self.fetched_values[stat][stat_key]
                
            goals_scored = self.get_goals_scored(h_a_specific=h_a_specific,
                                                 number_of_games=number_of_games,
                                                 from_date=from_date,
                                                 to_date=to_date)
            
            #get_goals_scored may return "Not enough games available"
            if type(goals_scored) == str:
                return goals_scored
            goals_conceded = self.get_goals_conceded(h_a_specific=h_a_specific,
                                                     number_of_games=number_of_games,
                                                     from_date=from_date,
                                                     to_date=to_date)
            
            #get_goals_conceded may return "Not enough games available"
            if type(goals_conceded) == str:
                return goals_conceded
            
            goal_difference = goals_scored-goals_conceded
            
            self.fetched_values[stat][stat_key] = goal_difference
            return goal_difference
        
    def get_goal_difference_per_game(self, h_a_specific="", number_of_games=0,
                                     seasons=[], from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_goal_difference_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 1000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total goal difference pg"
        elif h_a_specific.lower() == "home":
            stat = "home goal difference pg"
        elif h_a_specific.lower() == "away":
            stat = "away goal difference pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            goal_difference = self.get_goal_difference(h_a_specific=h_a_specific,
                                                       number_of_games=number_of_games,
                                                       from_date=from_date,
                                                       to_date=to_date)
            #get_goal_difference may return "Not enough games available"
            if type(goal_difference) == str:
                return goal_difference
            if goal_difference == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = goal_difference / number_of_games
                return goal_difference / number_of_games
    
    def get_points(self, h_a_specific="", number_of_games=0, seasons=[],
                   from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_points one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total points"
        elif h_a_specific.lower() == "home":
            stat = "home points"
        elif h_a_specific.lower() == "away":
            stat = "away points"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            wins = self.get_win_count(h_a_specific=h_a_specific,
                                            number_of_games=number_of_games,
                                            from_date=from_date,
                                            to_date=to_date)
            
            #get_win_count may return "Not enough games available"
            if type(wins) == str:
                return wins
            
            win_points = wins * 3
            
            draw_points = self.get_draw_count(h_a_specific=h_a_specific,
                                              number_of_games=number_of_games,
                                              from_date=from_date,
                                              to_date=to_date)
            
            #get_draw_count may return "Not enough games available"
            if type(draw_points) == str:
                return draw_points
            
            points = win_points+draw_points
            self.fetched_values[stat][stat_key] = points
            return points
            
    def get_points_per_game(self, h_a_specific="", number_of_games=0, seasons=[],
                            from_date=c.now, to_date=""):
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(number_of_games,seasons):
            print("#####")
            print("get_points_per_game: one_argument_error")
            print(h_a_specific,number_of_games,seasons)
            input()
            return 1
        
        if not to_date:
            #If no to_date has been set, set it to 20000 days before the from date.
            to_date = from_date-c.timedelta(days=20000)
            
        if not h_a_specific:
            stat = "total points pg"
        elif h_a_specific.lower() == "home":
            stat = "home points pg"
        elif h_a_specific.lower() == "away":
            stat = "away points pg"
            
        #Create a dictionary key specifically for this date and set of games.
        stat_key = (from_date.strftime("%d%m%y") + " - " +
                    to_date.strftime("%d%m%y") + " " + str(number_of_games) +
                    " games")
        
        if number_of_games:
            points = self.get_points(h_a_specific=h_a_specific,
                                     number_of_games=number_of_games,
                                     from_date=from_date,
                                     to_date=to_date)
            #get_points may return "Not enough games available"
            if type(points) == str:
                return points
            if points == 0:
                self.fetched_values[stat][stat_key] = 0
                return 0
            else:
                self.fetched_values[stat][stat_key] = points / number_of_games
                return points / number_of_games
            
    def get_data(self,home_away_total,scored_conceded, no_of_games=0, seasons=[]):
        """
        Takes a "home" "away" or "total" string, a "scored", "conceded" or
        "scored and conceded" string, either an int for number of games to go
        back over or a list of seasons to go back over.
        Returns the number of goals "scored", "conceded" or "scored and conceded"
        for the relevant string over the relvant number of games.
        """
        goal_count = 0
        home_goals_scored = 0
        away_goals_scored = 0
        total_goals_scored = 0
        home_goals_conceded = 0
        away_goals_conceded = 0
        total_goals_conceded = 0
        win_count = 0
        draw_count = 0
        loss_count = 0
        home_win_count = 0
        home_draw_count = 0
        home_loss_count = 0
        away_win_count = 0
        away_draw_count = 0
        away_loss_count = 0
        value_name = home_away_total+" goals " + scored_conceded
        
        #Ensure only one of no_of_games or seasons are passed
        if not c.one_argument(no_of_games, seasons):
            print("#####")
            print("get_data: one_argument error")
            print(home_away_total,scored_conceded, no_of_games, seasons)
            input()
            return 1
        
        #If the argument is the number of games
        if no_of_games:
            #print("NO_OF_GAMES")#DEBUG
            #Check if the requested value is already in the fetched_values dictionary.
            #If so, return the same result.
            if no_of_games in self.fetched_values[value_name].keys():
                #DEBUG
                #print("no_of_games is in fetched. no_of_games:")
                return self.fetched_values[value_name][no_of_games]
            
            #Reduce the size of the merged_data dataframe by only selecting rows that contain the team.
            df = c.merged_data.loc[(c.merged_data["HomeTeam"] == self.team_name) | 
                    (c.merged_data["AwayTeam"] == self.team_name)]
            home_game_count = 0
            away_game_count = 0
            game_count = 0
            #Get home values
            df = c.merged_data.loc[(c.merged_data["HomeTeam"] == 
                                    self.team_name)].head(no_of_games)
            home_goals_scored = df["FTHG"].sum()
            home_goals_conceded = df["FTAG"].sum()
            for index, row in df.iterrows():
                if row["FTHG"] == row["FTAG"]:
                    home_draw_count += 1
                if row["FTHG"] > row["FTAG"]:
                    home_win_count += 1
                if row["FTHG"] < row["FTAG"]:
                    home_loss_count += 1
                home_game_count = df.count()["HomeTeam"]
            
            #Get away values
            df = c.merged_data.loc[(c.merged_data["AwayTeam"] ==
                                    self.team_name)].head(no_of_games)
            away_goals_scored = df["FTAG"].sum()
            away_goals_conceded = df["FTHG"].sum()
            for index, row in df.iterrows():
                if row["FTHG"] == row["FTAG"]:
                    away_draw_count += 1
                if row["FTHG"] > row["FTAG"]:
                    away_loss_count += 1
                if row["FTHG"] < row["FTAG"]:
                    away_win_count += 1
                away_game_count = df.count()["AwayTeam"]
                    
            #Get total values
            df = c.merged_data.loc[((c.merged_data["HomeTeam"] == self.team_name) | 
                    (c.merged_data["AwayTeam"] == self.team_name))].head(no_of_games)
            df_home = df[(df["HomeTeam"] == self.team_name)]
            df_away = df[(df["AwayTeam"] == self.team_name)]
            total_goals_scored = df_home["FTHG"].sum() + df_away["FTAG"].sum()
            total_goals_conceded = df_home["FTAG"].sum() + df_away["FTHG"].sum()
            for index, row in df_home.iterrows():
                if row["FTHG"] == row["FTAG"]:
                    draw_count += 1
                if row["FTHG"] > row["FTAG"]:
                    win_count += 1
                if row["FTHG"] < row["FTAG"]:
                    loss_count += 1
            for index, row in df_away.iterrows():
                if row["FTHG"] == row["FTAG"]:
                    draw_count += 1
                if row["FTHG"] > row["FTAG"]:
                    loss_count += 1
                if row["FTHG"] < row["FTAG"]:
                    win_count += 1
            game_count = df.count()["HomeTeam"]

            #If too many games were passed as no_of_games       
            if home_away_total == "total" and game_count != no_of_games:
                print("Team - get_goals - More games specified than available")
                print("Goals from "+str(game_count)+" games returned")
                
            if home_away_total == "home" and home_game_count != no_of_games:
                print("Team - get_goals - More games specified than available")
                print("Goals from "+str(game_count)+" home games returned")
                
            if home_away_total == "away" and away_game_count != no_of_games:
                print("Team - get_goals - More games specified than available")
                print("Goals from "+str(game_count)+" away games returned")

            #Store the results in the fetched_values dictionary
            #Add requested counts to the goal_count.
            
            if home_game_count > 0:
                self.fetched_values["home wins pg"][game_count] = home_win_count / home_game_count
                self.fetched_values["home draws pg"][game_count] = home_draw_count / home_game_count
                self.fetched_values["home losses pg"][game_count] = home_loss_count / home_game_count
                self.fetched_values["home goals scored pg"][game_count] = home_goals_scored / home_game_count
                self.fetched_values["home goals conceded pg"][game_count] = home_goals_conceded / home_game_count
                self.fetched_values["home points pg"][game_count] = ((home_win_count * 3) + home_draw_count) / home_game_count
                self.fetched_values["home goal difference pg"][game_count] = (home_goals_scored - home_goals_conceded) / home_game_count
            else:
                self.fetched_values["home wins pg"][game_count] = 0
                self.fetched_values["home draws pg"][game_count] = 0
                self.fetched_values["home losses pg"][game_count] = 0
                self.fetched_values["home goals scored pg"][game_count] = 0
                self.fetched_values["home goals conceded pg"][game_count] = 0
                self.fetched_values["home points pg"][game_count] = 0
                self.fetched_values["home goal difference pg"][game_count] = 0
            
            if away_game_count > 0:
                self.fetched_values["away wins pg"][game_count] = away_win_count / away_game_count
                self.fetched_values["away draws pg"][game_count] = away_draw_count / away_game_count
                self.fetched_values["away losses pg"][game_count] = away_loss_count / away_game_count
                self.fetched_values["away goals scored pg"][game_count] = away_goals_scored / away_game_count
                self.fetched_values["away goals conceded pg"][game_count] = away_goals_conceded / away_game_count
                self.fetched_values["away points pg"][game_count] = ((away_win_count * 3) + away_draw_count) / away_game_count
                self.fetched_values["away goal difference pg"][game_count] = (away_goals_scored - away_goals_conceded) / away_game_count
            else:
                self.fetched_values["away wins pg"][game_count] = 0
                self.fetched_values["away draws pg"][game_count] = 0
                self.fetched_values["away losses pg"][game_count] = 0
                self.fetched_values["away goals scored pg"][game_count] = 0
                self.fetched_values["away goals conceded pg"][game_count] = 0
                self.fetched_values["away points pg"][game_count] = 0
                self.fetched_values["away goal difference pg"][game_count] = 0
            if game_count > 0:
                self.fetched_values["total wins pg"][game_count] = win_count / game_count
                self.fetched_values["total draws pg"][game_count] = draw_count / game_count
                self.fetched_values["total losses pg"][game_count] = loss_count / game_count
                self.fetched_values["total goals scored pg"][game_count] = (home_goals_scored + away_goals_scored) / game_count
                self.fetched_values["total goals conceded pg"][game_count] = (home_goals_conceded + away_goals_conceded) / game_count
                self.fetched_values["total points pg"][game_count] = ((win_count * 3) + draw_count) / game_count
                self.fetched_values["total goal difference pg"][game_count] = ((home_goals_scored + away_goals_scored) - (home_goals_conceded + away_goals_conceded)) / (home_game_count + away_game_count)
            else:
                self.fetched_values["total wins pg"][game_count] = 0
                self.fetched_values["total draws pg"][game_count] = 0
                self.fetched_values["total losses pg"][game_count] = 0
                self.fetched_values["total goals scored pg"][game_count] = 0
                self.fetched_values["total goals conceded pg"][game_count] = 0
                self.fetched_values["total points pg"][game_count] = 0
                self.fetched_values["total goal difference pg"][game_count] = 0
            
            self.fetched_values["home wins"][game_count] = home_win_count
            self.fetched_values["home draws"][game_count] = home_draw_count
            self.fetched_values["home losses"][game_count] = home_loss_count
            self.fetched_values["away wins"][game_count] = away_win_count
            self.fetched_values["away draws"][game_count] = away_draw_count
            self.fetched_values["away losses"][game_count] = away_loss_count
            self.fetched_values["total wins"][game_count] = home_win_count + away_win_count
            self.fetched_values["total draws"][game_count] = home_draw_count + away_draw_count
            self.fetched_values["total losses"][game_count] = home_loss_count + away_loss_count
            self.fetched_values["total goals scored"][game_count] = total_goals_scored
            self.fetched_values["total goals conceded"][game_count] = total_goals_conceded
            self.fetched_values["total goals scored and conceded"][game_count] = total_goals_scored + total_goals_conceded
            self.fetched_values["total goal difference"][game_count] = total_goals_scored - total_goals_conceded
            self.fetched_values["home goals scored"][game_count] = home_goals_scored
            self.fetched_values["home goals conceded"][game_count] = home_goals_conceded
            self.fetched_values["home goals scored and conceded"][game_count] = home_goals_scored + home_goals_conceded
            self.fetched_values["home goal difference"][game_count] = home_goals_scored - home_goals_conceded
            self.fetched_values["away goals scored"][game_count] = away_goals_scored
            self.fetched_values["away goals conceded"][game_count] = away_goals_conceded
            self.fetched_values["away goals scored and conceded"][game_count] = away_goals_scored + away_goals_conceded
            self.fetched_values["away goal difference"][game_count] = away_goals_scored - away_goals_conceded
            self.fetched_values["total played"][game_count] = home_game_count + away_game_count
            self.fetched_values["home points"][game_count] = (home_win_count * 3) + home_draw_count
            self.fetched_values["away points"][game_count] = (away_win_count * 3) + away_draw_count
            self.fetched_values["total points"][game_count] = (win_count * 3) + draw_count
            
            if home_away_total == "home" or home_away_total == "total":
                if scored_conceded == "scored" or scored_conceded == "scored and conceded":
                    goal_count += home_goals_scored
                if scored_conceded == "conceded" or scored_conceded == "scored and conceded":
                    goal_count += home_goals_conceded
            if home_away_total == "away" or home_away_total == "total":
                if scored_conceded == "scored" or scored_conceded == "scored and conceded":
                    goal_count += away_goals_scored
                if scored_conceded == "conceded" or scored_conceded == "scored and conceded": 
                    goal_count += away_goals_conceded
            #DEBUG
            #print(self.fetched_values[value_name])
            return goal_count
                        
        #loaded_data[league+" "+season] <-- Note for dictionary formatting
        
        #If the argument is a list of seasons
        if seasons:
            #print("SEASONS")#DEBUG
            for season in seasons:
                league_season = c.get_league(self.team_name, season)+" "+season
                #print(league_season)#DEBUG / DEV
                if league_season in c.loaded_data:
                    #print(league_season+" processing...")#DEBUG / Detail
                    
                    #Set the fetch flag to True meaning that by default
                    #the data will be scraped from the df.
                    fetch = True
                    
                    #Season counts
                    goals_this_season = 0
                    home_game_count = 0
                    away_game_count = 0
                    home_goals_scored = 0
                    home_goals_conceded = 0
                    away_goals_scored = 0
                    away_goals_conceded = 0
                    home_win_count = 0
                    home_draw_count = 0
                    home_loss_count = 0
                    away_win_count = 0
                    away_draw_count = 0
                    away_loss_count = 0
                    
                    #Check if league_season data in fetched_values dictionary
                    #If so, add the stored value to the counted goals_this_season
                    #and set the fetch flag to false.
                    if league_season in self.fetched_values[value_name].keys():
                        goals_this_season = self.fetched_values[value_name][league_season]
                        fetch = False
                    
                    #If the fetch flag is true the data wasn't in the fetched_data dictionary
                    #fetch the data from the dataframe and add it to the fetched_values dictionary.
                    if fetch:
                        #Reduce the size of the merged_data dataframe by only selecting rows that contain the team.
                        df = c.loaded_data[league_season].loc[(c.loaded_data[league_season]["HomeTeam"] == self.team_name) | (c.loaded_data[league_season]["AwayTeam"] == self.team_name)]
                        
                        for index, row in df.iterrows():

                            if row["HomeTeam"] == self.team_name:
                                home_goals_scored += row["FTHG"]
                                home_goals_conceded += row["FTAG"]
                                if row["FTHG"] == row["FTAG"]:
                                    home_draw_count += 1
                                if row["FTHG"] > row["FTAG"]:
                                    home_win_count += 1
                                if row["FTHG"] < row["FTAG"]:
                                    home_loss_count += 1
                                home_game_count += 1
                                #DEBUG CODE
                                #print("Home game ",row["Date"],row["HomeTeam"],row["FTHG"],row["AwayTeam"],row["FTAG"])
                                    
                            if row["AwayTeam"] == self.team_name:
                                away_goals_scored += row["FTAG"]
                                away_goals_conceded += row["FTHG"]
                                if row["FTHG"] == row["FTAG"]:
                                    away_draw_count += 1
                                if row["FTHG"] > row["FTAG"]:
                                    away_loss_count += 1
                                if row["FTHG"] < row["FTAG"]:
                                    away_win_count += 1
                                away_game_count += 1
                                #DEBUG CODE
                                #print("Away game ",row["Date"],row["HomeTeam"],row["FTHG"],row["AwayTeam"],row["FTAG"])
                                    
                        #Current season counts complete
                        #Add requested counts to total
                        if home_away_total == "home" or home_away_total == "total":
                            if scored_conceded == "scored" or scored_conceded == "scored and conceded":
                                goals_this_season += home_goals_scored
                            if scored_conceded == "conceded" or scored_conceded == "scored and conceded":
                                goals_this_season += home_goals_conceded
                        if home_away_total == "away" or home_away_total == "total":
                            if scored_conceded == "scored" or scored_conceded == "scored and conceded":
                                goals_this_season += away_goals_scored
                            if scored_conceded == "conceded" or scored_conceded == "scored and conceded": 
                                goals_this_season += away_goals_conceded
                        #Add this season's data to the fetched_values dictionary
                        self.fetched_values["home wins"][league_season] = home_win_count
                        if home_game_count > 0:
                            self.fetched_values["home wins pg"][league_season] = home_win_count / home_game_count
                            self.fetched_values["home draws pg"][league_season] = home_draw_count / home_game_count
                            self.fetched_values["home losses pg"][league_season] = home_loss_count / home_game_count
                            self.fetched_values["home goals scored pg"][league_season] = home_goals_scored / home_game_count
                            self.fetched_values["home goals conceded pg"][league_season] = home_goals_conceded / home_game_count
                            self.fetched_values["home goals scored and conceded pg"][league_season] = (home_goals_scored + home_goals_conceded) / home_game_count
                            self.fetched_values["home points pg"][league_season] = ((home_win_count * 3) + home_draw_count) / home_game_count
                            self.fetched_values["home goal difference pg"][league_season] = (home_goals_scored - home_goals_conceded) / home_game_count
                        else:
                            self.fetched_values["home wins pg"][league_season] = 0
                            self.fetched_values["home draws pg"][league_season] = 0
                            self.fetched_values["home losses pg"][league_season] = 0
                            self.fetched_values["home goals scored pg"][league_season] = 0
                            self.fetched_values["home goals conceded pg"][league_season] = 0
                            self.fetched_values["home goals scored and conceded pg"][league_season] = 0
                            self.fetched_values["home points pg"][league_season] = 0
                            self.fetched_values["home goal difference pg"][league_season] = 0
                            
                        if away_game_count > 0:
                            self.fetched_values["away wins pg"][league_season] = away_win_count / away_game_count
                            self.fetched_values["away draws pg"][league_season] = away_draw_count / away_game_count
                            self.fetched_values["away losses pg"][league_season] = away_loss_count / away_game_count
                            self.fetched_values["away goals scored pg"][league_season] = away_goals_scored / away_game_count
                            self.fetched_values["away goals conceded pg"][league_season] = away_goals_conceded / away_game_count
                            self.fetched_values["away goals scored and conceded pg"][league_season] = (away_goals_scored + away_goals_conceded) / away_game_count
                            self.fetched_values["away points pg"][league_season] = ((away_win_count * 3) + away_draw_count) / away_game_count
                            self.fetched_values["away goal difference pg"][league_season] = (away_goals_scored - away_goals_conceded) / away_game_count
                            
                        else:
                            self.fetched_values["away wins pg"][league_season] = 0
                            self.fetched_values["away draws pg"][league_season] = 0
                            self.fetched_values["away losses pg"][league_season] = 0
                            self.fetched_values["away goals scored pg"][league_season] = 0
                            self.fetched_values["away goals conceded pg"][league_season] = 0
                            self.fetched_values["away goals scored and conceded pg"][league_season] = 0
                            self.fetched_values["away points pg"][league_season] = 0
                            self.fetched_values["away goal difference pg"][league_season] = 0
                            
                        if home_game_count + away_game_count > 0:
                            self.fetched_values["total wins pg"][league_season] = (home_win_count + away_win_count) / (home_game_count + away_game_count)
                            self.fetched_values["total draws pg"][league_season] = (home_draw_count + away_draw_count) / (home_game_count + away_game_count)
                            self.fetched_values["total losses pg"][league_season] = (home_loss_count + away_loss_count) / (home_game_count + away_game_count)
                            self.fetched_values["total goals scored pg"][league_season] = (home_goals_scored + away_goals_scored) / (home_game_count + away_game_count)
                            self.fetched_values["total goals conceded pg"][league_season] = (home_goals_conceded + away_goals_conceded) / (home_game_count + away_game_count)
                            self.fetched_values["total goals scored and conceded pg"][league_season] = (home_goals_scored + home_goals_conceded + away_goals_scored + away_goals_conceded) / (home_game_count + away_game_count)
                            self.fetched_values["total points pg"][league_season] = ( ( (home_win_count + away_win_count) * 3) + (home_draw_count + away_draw_count) ) / (home_game_count + away_game_count)
                            self.fetched_values["total goal difference pg"][league_season] = ((home_goals_scored + away_goals_scored) - (home_goals_conceded + away_goals_conceded)) / (home_game_count + away_game_count)
                        else:
                            self.fetched_values["total wins pg"][league_season] = 0
                            self.fetched_values["total draws pg"][league_season] = 0
                            self.fetched_values["total losses pg"][league_season] = 0
                            self.fetched_values["total goals scored pg"][league_season] = 0
                            self.fetched_values["total goals conceded pg"][league_season] = 0
                            self.fetched_values["total goals scored and conceded pg"][league_season] = 0
                            self.fetched_values["total points pg"][league_season] = 0
                            self.fetched_values["total goal difference pg"][league_season] = 0
                            
                        self.fetched_values["home draws"][league_season] = home_draw_count
                        self.fetched_values["home losses"][league_season] = home_loss_count
                        self.fetched_values["away wins"][league_season] = away_win_count
                        self.fetched_values["away draws"][league_season] = away_draw_count
                        self.fetched_values["away losses"][league_season] = away_loss_count
                        self.fetched_values["total wins"][league_season] = home_win_count + away_win_count
                        self.fetched_values["total draws"][league_season] = home_draw_count + away_draw_count
                        self.fetched_values["total losses"][league_season] = home_loss_count + away_loss_count
                        self.fetched_values["total goals scored"][league_season] = home_goals_scored + away_goals_scored
                        self.fetched_values["total goals conceded"][league_season] = home_goals_conceded + away_goals_conceded
                        self.fetched_values["total goals scored and conceded"][league_season] = home_goals_scored + home_goals_conceded + away_goals_scored + away_goals_conceded
                        self.fetched_values["total goal difference"][league_season] = (home_goals_scored + away_goals_scored) - (home_goals_conceded + away_goals_conceded)
                        self.fetched_values["home goals scored"][league_season] = home_goals_scored
                        self.fetched_values["home goals conceded"][league_season] = home_goals_conceded
                        self.fetched_values["home goals scored and conceded"][league_season] = home_goals_scored + home_goals_conceded
                        self.fetched_values["home goal difference"][league_season] = home_goals_scored - home_goals_conceded
                        self.fetched_values["away goals scored"][league_season] = away_goals_scored
                        self.fetched_values["away goals conceded"][league_season] = away_goals_conceded
                        self.fetched_values["away goals scored and conceded"][league_season] = away_goals_scored + away_goals_conceded
                        self.fetched_values["away goal difference"][league_season] = away_goals_scored - away_goals_conceded
                        self.fetched_values["home played"][league_season] = home_game_count
                        self.fetched_values["away played"][league_season] = away_game_count
                        self.fetched_values["total played"][league_season] = home_game_count + away_game_count
                        self.fetched_values["home points"][league_season] = (home_win_count * 3) + home_draw_count
                        self.fetched_values["away points"][league_season] = (away_win_count * 3) + away_draw_count
                        self.fetched_values["total points"][league_season] = ((home_win_count + away_win_count) * 3) + (home_draw_count + away_draw_count)
                    
                    #Add the requested goals found this season to the goal_count so far
                    goal_count += goals_this_season
                    
                    #print(str(goals_this_season)+" "+value_name+" in "+league_season)
                    
                #else:
                    #print("Team method: get_home_goals - listed season: " + league_season + " not in loaded data")
            
            return goal_count

        
        