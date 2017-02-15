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

class OverwatchHistogramData(object):
    """
    Compressed histogram data array:
    Store only bins which are non-zero
    """

    def __init__(self):
        """
        Constructor, init empty compressed array
        """
        self.__nbins = 0
        self.__data = {}

    def SetNbinsTotal(self, nbins):
        """
        Setting the amount of bins of the
        original histograms.

        Needed to reconstruct the original size
        of the histogram
        
        :param nbins: Number of bins
        :type nbins: Int
        """
        self.__nbins = nbins

    def SetBin(self, number, value):
        """
        Set a non-zero bin value
        
        :param number: Bin number
        :type number: Int
        :param value: Value
        :type value: Float
        """
        self.__data[number] = value

    def MakeDict(self):
        """
        Creating dictionary representation with
        key and value of the compressed histogram
        data
        
        :return: Dictionary representation of the histogram data
        :rtype: Dictionary
        """
        return {"nbins":self.__nbins, "data": self.__data}

    def FromDict(self, inputdict):
        """
        
        :param inputdict: Dictionary representation of the histogram data
        :type inputdict: Dictionary
        """
        self.__nbins = inputdict["nbins"]
        self.__data = inputdict["data"]

class OverwatchHistogramAxis(object):
    """
    Compressed information about root
    TAxis

    Storing only data which is really needed
    in order to re-initialize the histogram
    """

    def __init__(self):
        """
        Constructor
        """
        super(self.__class__, self).__init__()
        self.__name = ""
        self.__title = ""
        self.__nbins = ""
        self.__min = None
        self.__max = None
        self.__binedges = []

    def SetName(self, name):
        """
        Set the name of the axis
        
        :param name: Name of the axis
        :type name: String
        """
        self.__name = name

    def SetTitle(self, title):
        """
        Set the axis title
        
        :param title: Title of the axis
        :type title: String
        """
        self.__title = title

    def SetNbins(self, nbins):
        """
        Set the number of bins of the axis
        
        :param nbins: Number of bins
        :type nbins: Int
        """
        self.__nbins = nbins

    def SetRange(self, xmin, xmax):
        """
        Set the axis range from min to max
        (linear binning)
        
        :param xmin: Minimum value of the axis range
        :type xmin: Float
        :param xmax: Maximum value of the axis range
        :type xmax: Float
        """
        self.__min = xmin
        self.__max = xmax

    def SetBinEdges(self, binedges):
        """
        Set the bin edges
        
        :param binedges: List of bin edges (ordered) for non-linear binning
        :type binedges: List
        """
        self.__binedges = binedges

    def Initialize(self, rootaxis):
        """
        Automatically initialize axis from a ROOT TAxis
        
        :param rootaxis: Input TAxis
        :type rootaxis: TAxis
        """
        self.SetName(rootaxis.GetName())
        self.SetTitle(rootaxis.GetTitle())
        self.SetNbins(rootaxis.GetNbins())
        xbins = rootaxis.GetXbins()
        if xbins.GetSize():
            for i in range(0, xbins.GetSize()):
                self.__binedges.append(xbins.GetAt(i))
        else:
            self.SetRange(rootaxis.GetXmin(), rootaxis.GetXmax())

    def FromDict(self, inputdict):
        """
        Initialize axis information from a dictionary
        
        :param inputdict: Dictionary with axis information
        :type inputdict: String
        """
        self.__name = inputdict["name"]
        self.__title = inputdict["title"]
        self.__nbins = inputdict["nbins"]
        self.__min = inputdict["xmin"]
        self.__max = inputdict["xmax"]
        self.__binedges = inputdict["binedges"]

    def MakeDict(self):
        """
        Create dictionary representation
        
        :return: Dictionary with axis information
        :rtype: Dictionary
        """
        return {"name": self.__name, "title": self.__title, "nbins": self.__nbins, "xmin": self.__min, "xmax": self.__max, "binedges": self.__binedges}

class OverwatchHistogramHeader(object):
    """
    Header information of a histogram share information for all histograms of the same 
    type (note: Not ROOT histogram type but data type as sent by the HLT). These information
    contain
    - Name of the histogram
    - Type of the histogram
    - Title of the histogram
    - Axis definitions
    As these information is the same for all histograms of the same type it can be extracted
    as a different class and shared among all histograms of the same type in a single document
    """

    def __init__(self):
        """
        Constructor
        """
        self.__type = ""
        self.__name = ""
        self.__title = ""
        self.__axes = {}

    def SetName(self, name):
        """
        Set the name of the histogram
        
        :param name: Name of the histogram
        :type name: String
        """
        self.__name = name

    def SetTitle(self, title):
        """
        Set the title of the histogram
        
        :param title: Title of the histogram
        :type title: String
        """
        self.__tite = title

    def SetType(self, histtype):
        """
        Set the histogram type

        It will be important later to reconstruct the histogram
        
        :param histtype: Type of the histogram
        :type histtype: String
        """
        self.__type = histtype

    def GetName(self):
        """
        Get the name of the histogram
        
        :return: Name of the histogram
        :rtype: String
        """
        return self.__name

    def GetTitle(self):
        """
        Get the title of the histogram
        
        :return: Title of the histogram
        :rtype: String
        """
        return self.__title

    def GetType(self):
        """
        Get the type of the histogram
        
        :return: Type of the histogram
        :rtype: String
        """
        return self.__type

    def InitAxis(self, direction, axis):
        """
        Initialize compressed axis information
        
        :param direction: Direction of the axis
        :type direction: String
        :param axis: Input axis
        :type axis: TAxis
        """
        compaxis = OverwatchHistogramAxis()
        compaxis.Initialize(axis)
        self.__axes[direction] = compaxis

    def Initialize(self, roothist):
        """
        Initialize header from ROOT histogram. Define
        - Name
        - Title
        - Typ

        Initialize axes
        
        :param roothist: Input histogram
        :type roothist: TH1, TH2 TH3
        """
        self.SetType(roothist.IsA().GetName())
        self.SetName(roothist.GetName())
        self.SetTitle(roothist.GetTitle())

        # Initialize axes
        if roothist.GetXaxis():
            self.InitAxis("x", roothist.GetXaxis())
        if roothist.GetYaxis():
            self.InitAxis("y", roothist.GetYaxis())
        if roothist.GetZaxis():
            self.InitAxis("z", roothist.GetZaxis())

    def MakeDict(self):
        """
        Get dictionary representation of the overwatch histogram header
        
        :return: Dictionary representation of the histogram header
        :rtype: Dictionary
        """
        axes = {}
        for k, v in self.__axes.iteritems():
            axes[k] = v.MakeDict()
        return {"type": self.__type, "name": self.__name, "title": self.__title, "axes": axes}
    
    def FromDict(self, inputdict):
        """
        Obtain histogram header from dictionary representation
        
        :param inputdict: input data as dictionary representation
        :type inputdict: Dictionary
        """
        self.__type = inputdict["type"]
        self.__name = inputdict["name"]
        self.__title = inputdict["title"]
        for k,v in inputdict["axes"].iteritems():
            myaxis = OverwatchHistogramAxis()
            myaxis.FromDict(v)
            self.__axes[k] = v

class OverwatchHistogram(object):
    """
    Compressed information of multi-dimensional histogram

    Storing only what is really needed in order to simply
    reconstruc the histogram from a JSON entry
    """

    def __init__(self):
        """
        Constructor
        """
        super(self.__class__, self).__init__()
        self.__header = OverwatchHistogramHeader()
        self.__data = OverwatchHistogramData()
        
        
    def SetHeader(self, header):
        """
        Set the histogram header
        
        :param header: Histogram header
        :type header: OverwatchHistogramHeader
        """
        self.__header = header
        
    def SetData(self, data):
        """
        Set the histogram data
        
        :param data: Histogram data
        :type data: OverwatchHistogramData
        """
        self.__data = data

    def SetName(self, name):
        """
        Set the name of the histogram
        
        :param name: Name of the histogram
        :type name: String
        """
        self.__header.SetName(name)

    def SetTitle(self, title):
        """
        Set the title of the histogram
        
        :param title: Title of the histogram
        :type title: String
        """
        self.__header.SetTitle(title)

    def SetType(self, histtype):
        """
        Set the histogram type

        It will be important later to reconstruct the histogram
        
        :param histtype: Type of the histogram (full type needed)
        :type histtype: String
        """
        self.__header.SetType(histtype)
        
    def GetHeader(self):
        """
        Get the histogram header
        
        :return: Histogram header
        :rtype: OverwatchHistogramHeader
        """
        return self.__header
    
    def GetData(self):
        """
        Get the histogram data
        
        :return: Histogram data
        :rtype: OverwatchHistogramData
        """
        return self.__data

    def GetName(self):
        """
        Get the name of the histogram
        
        :return: Type of the histogram (TH1, TH2, TH3)
        :rtype: String
        """
        return self.__header.GetName()

    def GetTitle(self):
        """
        Get the title of the histogram
        
        :return: Title of the histogram
        :rtype: String
        """
        return self.__header.GetTitle()

    def GetType(self):
        """
        Get the type of the histogram
        
        :return: Type of the histogram
        :rtype: String
        """
        return self.__header.GetType()

    def InitAxis(self, direction, axis):
        """
        Initialize compressed axis information
        
        :param direction: Direction of the axis
        :type direction: String
        :param axis: Axis information
        :type axis: TAxis
        """
        self.__header.InitAxis(direction, axis)

    def Initialize(self, roothist):
        """
        Fully initialize overatch histogram (type, name, title, axes, data)
        from underlying root histogram
        
        :param roothist: Intput histogram from roothist
        :type roothist: TH1, TH2 or TH3
        """
        self.__header.Initialize(roothist)

        # Initialize data points
        self.__data.SetNbinsTotal(roothist.GetNcells())
        for histbin in range(0, roothist.GetNcells()):
            value = float(roothist.GetBinContent(histbin))
            if abs(value) > 1e-12:
                self.__data.SetBin(histbin, value)

    def MakeDict(self):
        """
        Get dictionary representation of the overwatch histogram
        
        :return: Dictionary representation of the histogram
        :rtype: Dictionary
        """
        return {"header": self.__header.MakeDict(), "data": self.__data.MakeDict()}
    
    def FromDict(self, inputdict):
        """ 
        Convert dictionary into overwatch histogram. The dictionary has to follow the
        dictionary representation of an overwatch histogram.
        
        :param inputdict: Input data as dictionary representation
        :type inputdict: Dictionary
        """
        self.__header = OverwatchHistogramHeader()
        self.__Header.FromDict(inputdict["header"])
        self.__data = OverwatchHistogramData()
        self.__data.FromDict(inputdict["data"])
