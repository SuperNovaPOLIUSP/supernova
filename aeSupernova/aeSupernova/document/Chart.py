from File import *

class ChartError(Exception):
    """
     Exception reporting an error in the execution of a Chart operation.

    :version:
    :author:
    """
    pass

class Chart (File):
 
    """
     Base class for a chart.
  
    :version:
    :author:
    """
  
    """ ATTRIBUTES
  
     Dictionary of data to be displayed in the chart. Each amount of data in the
     dictionary must be indexed by a string which identifies it (e.g. in {'A' : 134},
     134 is the number of answers indexed by letter 'A', which is the question
     alternative marked for these answers).
  
    data  (public)
  
     Dictionary of labels to the data displayed by the chart. As it is done with the
     data attribute, it must also be indexed by a string which identifies it (e.g. in
     {'A' : "Very Good"}, "Very Good" is a label indexed by letter 'A', which is the
     question alternative that corresponds to this label).
  
    dataLabels  (public)
  
    """
  
    def __init__(self, data, dataLabels, directoryPath, fileName):
        """
         Constructor method.
  
        @param {} data : Dictionary of data to be displayed in the chart. Each amount of data in the dictionary must be indexed by a string which identifies it (e.g. in {'A' : 134}, 134 is the number of answers indexed by letter 'A', which is the question alternative marked for these answers).
        @param {} dataLabels : Dictionary of labels to the data displayed by the chart. As it is done with the data attribute, it must also be indexed by a string which identifies it (e.g. in {'A' : "Very Good"}, "Very Good" is a label indexed by letter 'A', which is the question alternative that corresponds to this label).
        @param string directoryPath : The absolute path to the directory which contains the file in the file system.
        @param string fileName : The file name (must not have spaces).
        @return  :
        @author
        """
        super(Chart, self).__init__(directoryPath, fileName)
        self.setData(data, False)
        self.setDataLabels(dataLabels, False)
        self.plot()
            
    def setData(self, data, plot = True):
        """
         Sets data attribute and plots the chart after doing so.
  
        @param {} data : Dictionary of data to be displayed in the chart. Each amount of data in the dictionary must be indexed by a string which identifies it. (e.g. {'A' : 134} 134 is the number of answers indexed by letter 'A', which is the question alternative marked for these answers).
        @param bool plot : Boolean that indicates if the chart should be plotted after setting the data attribute.
        @return  :
        @author
        """
        # verifies validity of data parameter
        if not isinstance(data, dict):
            raise ChartError("Invalid data parameter: must be a dictionary.")
        elif len(data) < 1:
            raise ChartError("Invalid data parameter: must not be an empty dictionary.")

        self.data = data
        
        # plots chart if instructed to do so
        if plot:
            self.plot()
  
    def setDataLabels(self, dataLabels, plot = True):
        """
         Sets dataLabels attribute and plots the chart after doing so.
  
        @param {} dataLabels : Dictionary of labels to the data displayed by the chart. As it is done with the data attribute, it must also be indexed by a string which identifies it (e.g. in {'A' : "Very Good"}, "Very Good" is a label indexed by letter 'A', which is the question alternative that corresponds to this label).
        @param bool plot : Boolean that indicates if the chart should be plotted after setting the dataLabels attribute.
        @return  :
        @author
        """
        # verifies validity of dataLabels parameter
        if not isinstance(dataLabels, dict):
            raise ChartError("Invalid dataLabels parameter: must be a dictionary.")
        elif len(dataLabels) < 1:
            raise ChartError("Invalid dataLabels parameter: must not be an empty dictionary.")

        self.dataLabels = dataLabels

        # plots chart if instructed to do so
        if plot:
            self.plot()
  
    def plot(self):
        """
         Plots the chart into a file (usually an image).
  
        @return  :
        @author
        """
        # abstract method
        pass

