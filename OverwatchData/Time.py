"""
Connector to the ALICE Overwatch histogram database based on Elasticsearch
Copyright (C) 2017  Markus Fasel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

class OverwatchTimestamp(object):
    """
    Class saving the time stamp as JSON document
    """

    def __init__(self, year = None, month = None, day = None, hours = None, minutes = None, seconds = None):
        """
        Constructor

        Optionally setting time information
        """
        super(self.__class__, self).__init__()
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds

    def SetYear(self, year):
        """
        Set the year
        
        :param year: Year
        :type year: Int
        """
        self.__year = year

    def SetMonth(self, month):
        """
        Set the month
        
        :param month: Month
        :type month: Int
        """
        self.__month = month

    def SetDay(self, day):
        """
        Set the day of the month
        
        :param day: Day of the month
        :type day: Int
        """
        self.__day = day

    def SetHours(self, hours):
        """
        Set the hours
        
        :param hours: Number of hours
        :type hours: Int
        """
        self.__hours = hours

    def SetMinutes(self, minutes):
        """
        Set the minutes
        
        :param minutes: Number of minutes
        :type minutes: Int
        """
        self.__minutes = minutes

    def SetSeconds(self, seconds):
        """
        Set the seconds
        
        :param second: Number of seconds
        :type seconds: Int
        """
        self.__seconds = seconds

    def GetYear(self):
        """
        Get the year
        
        :return: Year
        :rtype: Int
        """
        return self.__year

    def GetMonth(self):
        """
        Get the month
        
        :return: Month
        :rtype: Int
        """
        return self.__month

    def GetDay(self):
        """
        Get the day
        
        :return: Day of the month
        :rtype: Int
        """
        return self.__day

    def GetHours(self):
        """
        Get the hours
        
        :return: Number of hours
        :rtype: Int
        """
        return self.__hours

    def GetMinutes(self):
        """
        Get the minutes
        
        :return: Number of minutes
        :rtype: Int
        """
        return self.__minutes

    def GetSeconds(self):
        """
        Get the seconds
        
        :return: Number of seconds
        :rtype: Int
        """
        return self.__seconds
    
    def FromDict(self, inputdict):
        """
        Initialize time stamp from dictionary representation
        
        :param inputdict: Input data
        :type inputdict: Dictionary
        """
        self.__year = inputdict["year"]
        self.__month = inputdict["month"]
        self.__day = inputdict["day"]
        self.__hours = inputdict["hours"]
        self.__minutes = inputdict["minutes"]
        self.__seconds = inputdict["seconds"]

    def MakeDict(self):
        """
        Create dictionary representation of the timestamp
        
        :return: Dictionary representation of the timestamp
        :rtype: Dictionary
        """
        return {"year": self.__year, "month": self.__month, "day": self.__day, "hours": self.__hours, "minutes": self.__minutes, "seconds": self.__seconds}