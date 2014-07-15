# coding: utf8
from django.conf import settings
from File import *
from Chart import *

# modules for dealing with chart plotting
import os
os.environ['MPLCONFIGDIR'] = settings.PASTA_TEMPORARIA
import matplotlib
matplotlib.use('Agg')
import numpy.numarray as na
from pylab import *

class BarChartError(Exception):
    """
     Exception reporting an error in the execution of a BarChart operation.

    :version:
    :author:
    """
    pass

class BarChart (Chart):

    """
     Class that models a bar chart, providing operations to create and print a bar
     chart to an image.
  
    :version:
    :author:
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
        super(BarChart, self).__init__(data, dataLabels, directoryPath, fileName)
  
    def getTotalData(self):
        """
         Returns the sum of all of the data displayed in the chart (e.g. sum of all of
         the answers given to a question).
    
        @return int :
        @author
        """
        totalData = 0

        try:
            for datum in self.data.values():
                totalData += datum
        except:
            raise BarChartError("Failed to sum data. Perhaps one of the values in the data attribute dictionary is not a number.")

        return totalData
  
    def getPercentageData(self):
        """
         Returns a dictionary equivalent to the data attribute which keeps the data to be
         displayed by the chart. The dictionary returned by this method, however, keeps
         this data in a percentage format.
    
        @return {} :
        @author
        """
        
        totalData = self.getTotalData()

        # avoids division by zero
        if not totalData > 0:
            zero = True
        else:
            zero = False

        percentageData = {}

        try:
            for index, datum in self.data.items():
                if zero:
                    percentageData[index] = 0
                else:
                    percentageData[index] = 100 * float(datum) / float(totalData)
        except:
            raise BarChartError("Failed to calculate percentage data.")
        return percentageData
  
    def plot(self):
        """
         Implements abstract method from superclass.
         Plots the chart into a .png image file.
    
        @return  :
        @author
        """
        if 'A' not in self.data.keys():
            self.data['A'] = 0
        if 'B' not in self.data.keys():
            self.data['B'] = 0
        if 'C' not in self.data.keys():
            self.data['C'] = 0
        if 'D' not in self.data.keys():
            self.data['D'] = 0
        if 'E' not in self.data.keys():
            self.data['E'] = 0
        percentageData = self.getPercentageData()

        # preparation of the charts axis: they must be lists of the values that should be displayed in the chart

        # prepares charts X axis
        # defines X axis values according to the size of the labels
        labelMaxSize = max([len(label) for label in self.dataLabels.values()])
        if labelMaxSize < 25:
            # if the labels aren't too big, X axis receives the actual labels
            xAxisLabels = [self.dataLabels[chr(ord('A') + index)] for index in range(0, len(self.dataLabels))]
        else:
            # if the labels are too big, they receive the letter corresponding to the label
            xAxisLabels = [chr(ord('A') + index) for index in range(0, len(self.dataLabels))]
       
        # prepares charts Y axis
        yAxisData = {index : datum for index, datum in self.data.items() if index != 'X'} # removes null answers, as they should not be displayed
        n = len(yAxisData)
        yAxis = yAxisData
        yAxisData = []
        for index in range(0, n):
            char = chr(ord('A') + index)
            if char not in yAxis:
                yAxisData.append(0)
            else:
                yAxisData.append(yAxis[char])
        #yAxisData = [yAxisData[chr(ord('A') + index)] for index in range(0, len(yAxisData))]
        
        yAxisPercentageData = {index : percentageDatum for index, percentageDatum in percentageData.items() if index != 'X'} # removes null answers, as they should not be displayed
        n = len(yAxisPercentageData)
        yAxisPercentage = yAxisPercentageData
        yAxisPercentageData = []
        for index in range(0, n):
            char = chr(ord('A') + index)
            if char not in yAxisPercentage:
                yAxisPercentageData.append(0)
            else:
                yAxisPercentageData.append(yAxisPercentage[char])
        #yAxisPercentageData = [yAxisPercentageData[chr(ord('A') + index)] for index in range(0, len(yAxisPercentageData))]

        # verifies if the axis lengths are the same (this must be true for a bar chart)
        if len(yAxisData) != len(xAxisLabels):
            raise BarChartError("Axis length error: Y axis' data set (without null answers) must be of the same size as X axis' labels set")

        # defines a size factor based on the labels length
        if labelMaxSize > 20 and labelMaxSize < 25:
            sizeFactor = 4
        else:
            sizeFactor = 0.5

        # defines the axis's scales and bar sizes        
        barLength = 0.5
        xScale = 2 * barLength * na.array(range(len(xAxisLabels))) + barLength
        yScale = na.array(range(100))

        # creates the charts image and defines it size
        chartImage = figure(num = None, figsize = (12, 14), dpi = 100, facecolor = 'w', edgecolor = 'k')

        # plots the chart
        chart = chartImage.add_subplot(111)
        chartBars = chart.bar(xScale, yAxisPercentageData, width = barLength, color = 'gray', edgecolor = 'black', linewidth = 4)
        gcf().subplots_adjust(bottom = 0.15, left = -0.3)

        # puts numbers above bars
        for index in range(0, len(xAxisLabels)):
            barHeight = chartBars[index].get_height()
            chart.text(chartBars[index].get_x() + chartBars[index].get_width() / 2.0, barHeight + 1, str(yAxisData[index]), ha = 'center', va = 'bottom', fontsize = 54, fontweight = 'bold')
        # adds a grid to the chart
        gca().yaxis.grid(True, linewidth = 4)

        # puts X and Y axis labels values in the charts axis
        labelScale = na.array([xScale[i] - 0.1 * len(xAxisLabels[i]) / 4.0 for i in range(len(xAxisLabels))]) # defines a scale for the labels to be displayed in the axis, based on the length of each label
        xticks(labelScale, xAxisLabels, fontsize = int(-1.6842*sizeFactor + 36.8421), fontweight = 'bold', rotation = 25)
        yticks(fontsize = 42, fontweight = 'bold')

        # names the Y axis
        ylabel(u'Frequência Relativa (%)', fontsize = 56)

        # configures the axis scales
        ylim(0, 100)
        xlim(0, xScale[-1] + barLength * 2)

        # places the axis in the chart
        gca().get_xaxis().tick_bottom()
        gca().get_yaxis().tick_left()

        # puts the chart into a .png image file
        savefig(self.getAbsolutePath(), bbox_inches = 'tight', dpi = (22))

        self.fileName += '.png'
