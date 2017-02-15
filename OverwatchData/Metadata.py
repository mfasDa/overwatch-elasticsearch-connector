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

class OverwatchDetectorDescriptor:
    """
    Descriptor for the collection of histograms
    from a given detector (merger)
    """

    def __init__(self, detname = ""):
        """
        Initialize collection
        
        :param detname: Name of the detector
        :type detname: String
        """
        self.__detector = detname
        self.__histlist = []

    def __cmp__(self, other):
        """
        Comparator

        Comparison based on name of the detector. Logic
        delegated to comparison magic members
        """
        if self == other:
            return 0
        if self > other:
            return 1
        return -1

    def __eq__(self, other):
        """
        Check for equalness

        Comparison is based on the name of the detector.
        Implemented comparisons:
        - String
        - DetectorHistogramCollection
        """
        return self.__detector == self.__GetOtherName(other)

    def __lt__(self, other):
        """
        Check if this object is smaller than the other
        object

        Comparison is based on the name of the detector.
        Implemented comparisons:
        - String
        - DetectorHistogramCollection
        """
        return self.__detector < self.__GetOtherName(other)

    def __gt__(self, other):
        """
        Check if this object is smaller than the other
        object

        Comparison is based on the name of the detector.
        Implemented comparisons:
        - String
        - DetectorHistogramCollection
        """
        return self.__detector > self.__GetOtherName(other)

    def __GetOtherName(self, other):
        """
        Helper function obtaining the
        string for the comparison
        
        :param other: Object to obtain the name from
        :type other: String or OverwatchDetectorDescriptor
        """
        othername = ""
        if isinstance(other, str):
            othername = other
        if isinstance(other, OverwatchDetectorDescriptor):
            othername = other.GetName()
        return othername

    def SetDetector(self, det):
        """
        Set the name of the detector
        
        :param det: Name of the detector
        :type det: String
        """
        self.__detector = det

    def GetDetector(self):
        """
        Get the name of the detector
        
        :return: Name of the detector
        :rtype: String
        """
        return self.__detector

    def AddHistogram(self, histname):
        """
        Add new histogram to the
        desciptor (only in case it was not found)
        
        :param histname: Name of the histogram
        :type histname: String
        """
        if not histname in self.__histlist:
            self.__histlist.append(histname)

    def GetListOfHistograms(self):
        """
        Get the list of histograms
        the detector has sent for a given run
        
        :return: List of histograms in the detector descriptor
        :rtype: List
        """
        return self.__histlist

    def HasHistorgam(self, histname):
        """
        Check whether the detector has
        sent a certain histogram for
        the given run
        
        :param histname: Name of the histogram to find in the detector descriptor
        :type histname: String
        :return: True if the histogram was found in the detector descriptor
        :rtype: Bool
        """
        return histname in self.__histlist

    def MakeDict(self):
        """
        Create dictionary representation
        of the detector descriptor
        
        :return: Dictionary representation of the detector descriptor
        :rtype: Dictionary
        """
        return {"detector": self.__detector, "histograms": self.__histlist}

    def FromDict(self, inputdict):
        """
        Create detector descriptor form directory representation
        
        :param inputdict: Input dictionary
        :type inputdict:
        """
        self.__detector = inputdict["detector"]
        self.__histlist = inputdict["histograms"]

class OverwatchRunDescriptor:
    """
    Descriptor for run-based information
    """
    
    def __init__(self, runnumber = -1):
        """
        Constructor
        
        :param runnumber: run number
        :type runnumber: Int
        """
        self.__runnumber = runnumber
        self.__detectors = []

    def SetRunNumber(self, runnumber):
        """
        Set the run number
        
        :param runnumber: run number
        :type runnumber: Int
        """
        self.__runnumber = runnumber

    def AddDetector(self, detector):
        """
        Add new detector to the list of detectors
        Detector will only be added if not found
        
        :param detector: Name of the detector / histogram group
        :type detector: String
        """
        if not detector in self.__detectors:
            self.__detectors.append(OverwatchDetectorDescriptor(detector))
    
    def InsertDetectorDescriptor(self, detector):
        """
        Add fully-configured detector descriptor to the list of
        detectors
        
        :param detector: Detector descriptor to be added to the list of detectors
        :type detector: OverwatchDetectorDescriptor
        """
        self.__detectors.append(detector)

    def AddHistogramForDetector(self, detector, histogram):
        """
        Adding histogram to the detector

        Creating a new detector collection in case the
        detector is not yet preset.
        
        :param detector: Name of the detector for which to add the histogram
        :type detector: String
        :param histogram: Name of the histogram to be added
        :type histogram: String
        """
        if not detector in self.__detectors:
            det = OverwatchDetectorDescriptor(detector)
            det.AddHistogram(histogram)
            self.__detectors.append(det)
        else:
            mydet = self.__detectors[self.__detectors.index(detector)]
            mydet.AddHistogram(histogram)

    def MakeDict(self):
        """
        Create dictionary representation
        
        :return: Dictionary representation of the run descriptor
        :rtype: Dictionary
        """
        detlist = []
        for d in self.__detectors:
            detlist.append(d.MakeDict())
        return {"run": self.__runnumber, "detectors": detlist}

    def FromDict(self, inputdict):
        """
        Create run descriptor from dictionary representation
        
        :param inputdict: Input dictionary with run descriptor information
        :type inputdict: Dictionary
        """
        self.__runnumber = inputdict["run"]
        self.__detlist = []
        for d in inputdict["detectors"]:
            mydet = OverwatchDetectorDescriptor()
            mydet.FromDict(d)
            self.InsertDetectorDescriptor(mydet)
