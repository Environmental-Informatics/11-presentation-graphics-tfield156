#!/bin/env python
# Add your own header comments
#
'''
This script uses the raw data files for the Tippecannoe River and Wildcat Creek,
as well as the annual and monthly metrics from Lab 10. Several functions are copied
from Lab 10 to ease the input of data. After all data is read in, this script creates
six figures as PNG images to be used for presentation graphics. The font size on
all images is set to 22 to ensure that they are easy to read. Additionally, the
DPI is forced to be 96 so the images remain crisp when transferred to PowerPoint.

@authors: tfield
@github: tfield156
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "agency_cd", "site_no", "Date", "Discharge", "Quality". The 
    "Date" column should be used as the DataFrame index. The pandas read_csv
    function will automatically replace missing values with np.NaN, but needs
    help identifying other flags used by the USGS to indicate no data is 
    availabiel.  Function returns the completed DataFrame, and a dictionary 
    designed to contain all missing value counts that is initialized with
    days missing between the first and last date of the file."""
    
    # define column names
    colNames = ['agency_cd', 'site_no', 'Date', 'Discharge', 'Quality']

    # open and read the file
    DataDF = pd.read_csv(fileName, header=1, names=colNames,  
                         delimiter=r"\s+",parse_dates=[2], comment='#',
                         na_values=['Eqp'])
    DataDF = DataDF.set_index('Date')
    
    # remove negative streamflow as gross error check
    DataDF['Discharge'].loc[(DataDF['Discharge'] < 0)] = np.NaN
    
    # quantify the number of missing values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )

def ClipData( DataDF, startDate, endDate ):
    """This function clips the given time series dataframe to a given range 
    of dates. Function returns the clipped dataframe and and the number of 
    missing values."""

    # select only rows between the start and end dates (inclusive end points)
    DataDF = DataDF[startDate:endDate]
    
    # quantify the number of missing values
    MissingValues = DataDF["Discharge"].isna().sum()
    
    return( DataDF, MissingValues )
    
def ReadMetrics( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    the metrics from the assignment on descriptive statistics and 
    environmental metrics.  Works for both annual and monthly metrics. 
    Date column should be used as the index for the new dataframe.  Function 
    returns the completed DataFrame."""
    
    # read in the CSV files created in Lab 10 containing statistics on different time periods
    DataDF = pd.read_csv(fileName,index_col='Date',parse_dates=[0])
    return( DataDF )
    
def GetMonthlyAverages(MoDataDF):
    """This function calculates annual average monthly values for all 
    statistics and metrics.  The routine returns an array of mean values 
    for each metric in the original dataframe."""
    
    dates = MoDataDF.index #dates of each monthly statistic
    
    MonthAVG = []
    for i in range(12): #for each month
        MonthAVG.append(MoDataDF.loc[dates.month == (i+1)].mean()) #average of statistics for that month
        
    # create dataframe for all of the months
    MonthlyAverages = pd.DataFrame({1:MonthAVG[0],2:MonthAVG[1],
                                    3:MonthAVG[2],4:MonthAVG[3],
                                    5:MonthAVG[4],6:MonthAVG[5],
                                    7:MonthAVG[6],8:MonthAVG[7],
                                    9:MonthAVG[8],10:MonthAVG[9],
                                    11:MonthAVG[10],12:MonthAVG[11]})
    
    return( MonthlyAverages )

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    # define full river names as a dictionary so that abbreviations are not used in figures
    riverName = { "Wildcat": "Wildcat Creek",
                  "Tippe": "Tippecanoe River" }
    # Import data from raw files
    wildcatDF, MV = ReadData('WildcatCreek_Discharge_03335000_19540601-20200315.txt')
    tippeDF, MV = ReadData('TippecanoeRiver_Discharge_03331500_19431001-20200315.txt')
    
    #Import statistics from Lab 10
    annualMetrics = ReadMetrics('Annual_Metrics.csv')    
    monthlyMetrics = ReadMetrics('Monthly_Metrics.csv')
    
    # Clip raw data to correct time range, only keep discharge
    wildcatDF, MV = ClipData(wildcatDF, '1969-10-01', '2019-09-30' )
    tippeDF, MV = ClipData(tippeDF, '1969-10-01', '2019-09-30' )
    wildcatDF = wildcatDF['Discharge']
    tippeDF = tippeDF['Discharge']
    # Daily flow for last 5 years on record
    lastDate=wildcatDF.index[-1]
    startDate = lastDate - pd.DateOffset(months=(5*12)) #five years before
    
    # set font size on figures
    plt.rcParams.update({'font.size': 20})
    
    # Last five years of daily discharge
    plt.figure(figsize=(9,6.5))
    wildcatDF[startDate:lastDate].plot(style='r')
    tippeDF[startDate:lastDate].plot(style='b')
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('Discharge (ft^3/s)')
    plt.title('Last Five Years of Daily Discharge - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('DailyDischarge5Year.png',dpi=96)
    
    # Annual coefficient of variation
    plt.figure(figsize=(9,6.5))
    annualMetrics['Coeff Var'].loc[annualMetrics['Station'] == 'Wildcat'].plot(style='r')
    annualMetrics['Coeff Var'].loc[annualMetrics['Station'] == 'Tippe'].plot(style='b')
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('Coefficient of Variation (%)') #seems like a percent since *100
    plt.title('Annual Coefficient of Variation  - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('AnnualCoeffVar.png',dpi=96)
    
    # Annual TQmean
    plt.figure(figsize=(9,6.5))
    annualMetrics['Tqmean'].loc[annualMetrics['Station'] == 'Wildcat'].plot(style='r')
    annualMetrics['Tqmean'].loc[annualMetrics['Station'] == 'Tippe'].plot(style='b')
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('TQmean (UNITLESS)')
    plt.title('Annual TQ Mean - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('AnnualTQmean.png',dpi=96)
    
    #Annual R-B Index
    plt.figure(figsize=(9,6.5))
    annualMetrics['R-B Index'].loc[annualMetrics['Station'] == 'Wildcat'].plot(style='r')
    annualMetrics['R-B Index'].loc[annualMetrics['Station'] == 'Tippe'].plot(style='b')
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('R-B Index (UNITLESS)')
    plt.title('Annual R-B Index - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('AnnualRBindex.png',dpi=96)
    
    # Get monthly averages
    monthlyAVGwildcat = GetMonthlyAverages(monthlyMetrics.loc[monthlyMetrics['Station']=='Wildcat']).transpose()
    monthlyAVGtippe = GetMonthlyAverages(monthlyMetrics.loc[monthlyMetrics['Station']=='Tippe']).transpose()
    # Plot monthly mean flow
    plt.figure(figsize=(9,6.5))
    monthlyAVGwildcat['Mean Flow'].plot(style='r')
    monthlyAVGtippe['Mean Flow'].plot(style='b')
    plt.grid(True)
    plt.xlabel('Month Number')
    plt.ylabel('Mean Flow (ft^3/s)')
    plt.title('Monthly Mean Flow - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('MonthlyMeanFlow.png',dpi=96)
    
    # Exceedance Probability
    peakWildcat = annualMetrics['Peak Flow'].loc[annualMetrics['Station']=='Wildcat']
    peakTippe = annualMetrics['Peak Flow'].loc[annualMetrics['Station']=='Tippe']
    # sort descending for each dataset
    peakWildcat = peakWildcat.sort_values(ascending=False)
    peakTippe = peakTippe.sort_values(ascending=False)
    
    # plotting position, calculate Weibull distribution
    ppWildcat = []
    ppTippe = []
    for i in range(len(peakWildcat)):
        ppWildcat.append((i+1)/len(peakWildcat))
    for i in range(len(peakTippe)):
        ppTippe.append((i+1)/len(peakTippe))
    
    # Plot exceedance probability
    plt.figure(figsize=(9,6.5))
    plt.plot(ppWildcat, peakWildcat, '.r',markersize=12)
    plt.plot(ppTippe,peakTippe, '.b',markersize=12)
    plt.xlim(1,0)
    #exceedTippe.plot(style='b')
    plt.grid(True)
    plt.xlabel('Exceedance Probability')
    plt.ylabel('Peak Flow (ft^3/s)')
    plt.title('Peak Flow Probability - Field')
    plt.legend([riverName['Wildcat'],riverName['Tippe']],loc='best')
    plt.tight_layout()
    plt.savefig('ExceedanceProbability.png',dpi=96)
    
    
    
    
    
    
    
    
    
    
    
    
    