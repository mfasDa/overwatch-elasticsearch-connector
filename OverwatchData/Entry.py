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

class Entry():
    """ 
    Full datapoint representation of a histogram entry.
    """
    
    def __init__(self, det = None, datatype = None, run = None, histogram):
        """
        Constructor
        """
        self.__detector = det
        self.__datatype = datatype
        self.__run = run
        self.__time = None
        self.__histogram = None
        
    def GetRunNumber(self):
        return self.__run
    
    def GetDetector(self):
        return self.__detector
    
    def GetDataType(self):
        return self.__datatype
        
    def GetHistogramHeader(self):
        return self.__histogram.GetHeader()
    
    def GetHistogramData(self):
        return self.__histogram.GetData()
    
    def GetTime(self):
        return self.__time
    
    def GetDataIndex(self):
        return "alice_overwatchdata_%s_%d" %(self.__detector, self.__run)
    
    def GetHeaderIndex(self):
        return "alice_overwatchmeta_histogram"
    
    def GetDataDict(self):
        return {"time" : self.__time, "data": self.__histogram.GetData()}
    
    def SetRunNumber(self, run):
        self.__run = run
        
    def SetDetector(self, detector):
        self.__detector = detector
        
    def SetDataType(self, datatype):
        self.__datatype = datatype
        
    def SetTime(self, entrytime):
        self.__time = entrytime
        
    def SetHistogram(self, histogram):
        self.__histogram = histogram