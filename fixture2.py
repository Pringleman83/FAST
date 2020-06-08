# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:27:25 2019

@author: david
"""
import common_functions as c
class Fixture(object):
    def __init__(self, home_team, away_team, date, time):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.time = time
        #print("Date", date)
        #print("Time", time)
        #print("Home Team", home_team)
        #print("Away Team", away_team)
        self.detail = date.strftime("%d/%m/%Y") + ": " + home_team + " - " + away_team
        self.previous_encounters_specific = c.previous_encounters(home_team,
                                                                  away_team,
                                                                  True)
        
        self.previous_encounters_non_specific = c.previous_encounters(home_team,
                                                                      away_team,
                                                                      False)
    
    def get_last_x_comparison(self, number_of_games, from_date=c.now,
                              to_date="", season = ""):
        """
        Takes a number of games to go back.
        Takes an optional from date (datetime object) for testing on previous fixtures.
        Takes an optional to date (datetime object) for determining how far to go back time wise.
        Returns a comparison of home team home goal difference vs away team away goal difference.
        Returned value is a list containing a number and a string.
        The number is the goal difference between the two values (positive).
        The string is the name of the team favour lies with or "draw"
        """
            
        #print(to_date, from_date)
        if not to_date:
            #If no to_date has been set, set it to 1000 days before the from date.
            to_date = from_date-c.timedelta(days=1000)
            
        """if number_of_games > 5:
            print("Fixture - \"get_last_x_comparison\" method - Too many games passed")
            return 1"""
        
        # get comparison of goal differences for last x home team home games and away team away games.
        home_team_last_x_home_gd = (c.team_objs[self.home_team].get_goal_difference(
                h_a_specific="home", from_date=from_date, to_date=to_date,
                number_of_games=number_of_games))
        
        away_team_last_x_away_gd = (c.team_objs[self.away_team].get_goal_difference(
                h_a_specific="away", from_date=from_date, to_date=to_date,
                number_of_games=number_of_games))
        
        h_a_last_x_gd = home_team_last_x_home_gd - away_team_last_x_away_gd
        h_a_last_x_favour = "draw"
        if h_a_last_x_gd > 0:
            h_a_last_x_favour = self.home_team
        if h_a_last_x_gd < 0:
            h_a_last_x_favour = self.away_team
        h_a_last_x_gd_abs = abs(h_a_last_x_gd)
        return [h_a_last_x_gd_abs, h_a_last_x_favour]
    
