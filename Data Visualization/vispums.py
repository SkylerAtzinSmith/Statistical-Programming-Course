#////////////////////////////////////////////////////////////////////////////////////////////////////																							
#Name:                  Skyler Smith, Daniel Zapotoczny, Jacob Kerschner
#Date:                  10-Oct-2020
#Course Name:			DATA 51100 | Statistical Programming										
#Semester:				Fall I 2020																
#Assignment Name:		PROGRAMMING ASSIGNMENT #6													
#Program Name:			vispums																																										
#////////////////////////////////////////////////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------------------------
# This program is used to visualize Public-Use Microdata Samples (PUMS) 
#----------------------------------------------------------------------------------------------------
#////////////////////////////////////////////////////////////////////////////////////////////////////

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # used to format axis values
import numpy as np


# Load the 2013 PUMS dataset into dataFrame
def load_file():
    pums_data = pd.read_csv('ss13hil.csv')
    return pums_data

# Collect Language Data values and labels
def get_langdata(pums_data):
    languages = pums_data['HHL'].value_counts()

    labels = []
    sizes = []

    for i in range(1, len(languages) + 1):
        if i == 1:
            labels.append('English Only')
        elif i == 2:
            labels.append('Spanish')
        elif i == 3:
            labels.append('Other Indo-European')
        elif i == 4:
            labels.append('Asian and Pacific Island Languages')
        elif i >= 5:
            labels.append('Other')

        sizes.append(int(languages[i]))

    return sizes, labels

# clean HINCP for logrithmic plotting
def clean_HINCPdata(data):
    
    # Clean data for logscale histogram    
    data.fillna(1, inplace=True)
    data.replace(0, 1, inplace=True)
    pums_data[data < 0]['HINCP'] = 1

    
def histoplot(axs, data, chart_title, x_title):
    
    # Plot KDE plot on uncleaned data since it ignores null values and needs to take negatives and 0 val into account
    data.plot(kind='kde', ax=axs, color='k', ls='--')

    #clean the data
    clean_HINCPdata(data)
    
    # Make logspaced bins by spacing 100 bins between 1*10^1 - 1*10^7
    logbins=np.logspace(1, 7, num=100)

    # Set xscale to log and plot histogram with logspaced bins. Make density plot so that data is normalized
    axs.set_xscale("log")
    axs.hist(data, bins=logbins, facecolor='g', alpha=0.5, density=True)
    axs.title.set_text(chart_title)
    axs.set_xlabel(x_title + '- Log Scaled')
    axs.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.6f'))
    axs.grid()
    
# Plot Pie Chart to designated subplot using standard colors
def plotpie(axs, data, labels, title):
       
    axs.pie(piedat, startangle=-118, radius=1.2)

    axs.title.set_text(title)

    axs.legend(pielabs, loc='upper left')
    plt.axis('equal')

def plotbar(axs, data, chart_title, x_title, y_title):
    
    # Pull the possible number of vehicles for each Household, then sort ascending
    veh = data.unique()
    veh.sort()
    
    # Make a list to hold the number of households that own each vehicle
    sumvals = []

    # sum the number of households for each number of vehicles, div by 1k, add to list
    for i in veh:
        number = pums_data[data==i]['WGTP'].sum()/1000
        sumvals.append(number)

    # plot the values and add titles
    axs.bar(veh, sumvals, color='red', alpha=0.7)
    axs.title.set_text(chart_title)
    axs.set_xlabel(x_title)
    axs.set_ylabel(y_title)

def plotbub(axs, x_data, y_data, size_data, color_data, chart_label, x_label, y_label, colorbar_label):
    
    # Make a dict to map raw data placeholders to tax amount group
    amts = [0, 1]
    amts = np.concatenate([amts, np.arange(50, 1000, 50)])
    nextrange = np.arange(1000, 5000, 100)
    amts = np.concatenate([amts, nextrange])
    amts = np.append(amts, values=[5000, 5500, 6000, 7000, 8000, 9000, 10000])

    taxpvals = np.arange(68)+1
    
    taxdict = dict(zip(taxpvals, amts))
    
    y_data.replace(taxdict, inplace=True)

    # Plot the bubble plot, add colorbar, and format axes
    sctplt = axs.scatter(x_data, y_data, s = size_data, c = color_data, cmap='seismic', marker='o', alpha=0.2)
    clrbr = plt.colorbar(sctplt)
    axs.set_aspect('auto')
    axs.set_xlim(0, 1200000)
    axs.set_ylim(0)

    # Set labels for chart elements
    clrbr.set_label(colorbar_label+' (Monthly $)')
    axs.title.set_text(chart_label)
    axs.set_xlabel(x_label+'($)')
    axs.set_ylabel(y_label+'($)')
    
    # Turn off scientific Notation
    axs.ticklabel_format(style='plain')



# Load the PUMS data and make a figure with 2x2 subplots
pums_data = load_file()
fig, axs = plt.subplots(2, 2)

# Make the figure bigger
fig.set_figheight(16)
fig.set_figwidth(22)

# Denote Axes
ax1=axs[0,0]
ax2=axs[0,1]
ax3=axs[1,0]
ax4=axs[1,1]

# Load language data into variables to make pie chart
piedat, pielabs = get_langdata(pums_data)

# Plot piechart of language data
plotpie(ax1, piedat, pielabs, 'Household Languages')

# Plot normalized histogram of Household Income
histoplot(ax2, pums_data['HINCP'], 'Distribution of Household Income', 'Household Income($)')

# Plot barchart of vehicles per thousands of households
plotbar(ax3, pums_data['VEH'],'Vehicles Available in Households', '# of Vehicles', 'Thousands of Households')

# plot the bubble plot with specified data
plotbub(ax4, pums_data['VALP'], pums_data['TAXP'], pums_data['WGTP'], pums_data['MRGP'], 'Property Taxes vs Property Values','Property Value', 'Taxes', 'First Mortgage Payment')

# save the figure to png
fig.savefig('pums.png')