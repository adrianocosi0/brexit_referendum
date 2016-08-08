#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from lxml.html import parse
from urllib2 import urlopen
from pandas.io.parsers import TextParser

parsed = parse(urlopen('https://ig.ft.com/sites/elections/2016/uk/eu-referendum/'))
doc = parsed.getroot()
tables = doc.findall('.//table')

#function to extract row elements from table row

def unpack(rows, kind='td'):
	elts = rows.findall('.//{}'.format(kind))
	return [a.text_content().strip() for a in elts]

#function to parse votes' website data to DataFrame

def extract_votes_data(tab):
	rows = tab.findall('.//tr')
	header = unpack(rows[0], 'th')
    #each unpacked row is converted into an array to allow for explicit indexing. the row is then reconverted into a list
	values = [list(np.array(unpack(row))[[0,2,3]]) for row in rows[1:]]
	#TextParser is an iterable object, get_chunk method returns all rows by default
	return TextParser(values, names=['Borough']+header[3:], thousands=',').get_chunk()

referendum_votes = extract_votes_data(tables[0]).set_index('Borough')

#method to substitute total numbers with percentages and rename columns of a dataframe
def comp_percent(frame, total_column):
    for col in frame.columns[:-1]:
        frame[col] = frame[col]/frame[total_column]
        frame.rename(index=str, columns={col:'%' + " " + col})

#add Total Column to apply method

referendum_votes['Total'] = referendum_votes.sum(axis=1)

comp_percent(referendum_votes, 'Total')

'''the dataframe for referendum votes contains boroughs for all UK but later, when the dataframes are merged,
these will be discarded'''

'''Proceed to parse excel data into dataframe. Data comes from gov.uk,it 
is by London neighbourhood and datasets cover: fear of crime, ethnicity, 
average earnings, mayor elections total votes by parties (democratic, liberal, green).
Data comes in xls format'''

mayor_votes = pd.ExcelFile('projects/referendum votes/raw data/gla-elections-votes-all-2016.xls')

mayor_votes = pd.read_excel(mayor_votes, sheetname='Boroughs', parse_cols=[0,3,4,5,62,63,64,65,66,67,68,69,70], skip_rows=34)

mayor_votes = mayor_votes.set_index('Borough')
#the boroughs containing & are renamed to allow for merging. the entries would drop otherwise
mayor_votes = mayor_votes.rename(index={'Barking & Dagenham':'Barking and Dagenham', 'Hammersmith & Fulham': 'Hammersmith and Fulham',
								'Kensington & Chelsea':'Kensington and Chelsea'})

Turnout = mayor_votes['% Turnout']

Turnout.index = mayor_votes.index

#endpoint is inclusive with label indexing
for a in ['Turnout', 'Ward Level Electorate', '% Turnout']:
	del mayor_votes[a]

comp_percent(mayor_votes, 'Total Good')

'''Parse fear of crime data'''

fear_of_crime_data = pd.ExcelFile('projects/referendum votes/raw data/MASTER_mps-figures_new.xls')

fear_crime = pd.read_excel(fear_of_crime_data, sheetname='Fear of Crime-Borough', skip_rows=[0,1], header=2)

fear_crime.head()

#only the most recent period is relevant for the analysis and would like to index the dataframe by borough

fear_crime = fear_crime.ix[31,1:]

'''Parse ethnicity data'''

ethnicity_data = pd.ExcelFile('projects/referendum votes/raw data/ethnic-groups-by-borough.xls')

#is the skip_rows needed or not? try without
ethnicity_data = pd.read_excel(ethnicity_data, sheetname='2014', index_col='Area', thousands=',')

del ethnicity_data['Code']

ethnicity_data = ethnicity_data.dropna()

ethnicity_data.loc['City of London'] = np.NaN

comp_percent(ethnicity_data, 'Total')

'''Parse earnings data'''

earnings_data = pd.ExcelFile('projects/referendum votes/raw data/earnings-residence-borough.xls')

#is the skip_rows needed or not? try without
earnings = pd.read_excel(earnings_data, sheetname='Total, weekly', skip_rows=[0,1], header = 2, parse_cols = [1,28,29,30])

earnings.loc['City of London'] = np.NaN

earnings.dropna()

'''Proceed to merge all data in a dataframe'''

frames = [referendum_votes, mayor_votes, ethnicity_data, earnings]

series = [fear_crime, Turnout]

#merge on dataframes
a = reduce(lambda x,y: x.merge(y, how='inner', suffixes=('x','y'), left_index=True, right_index=True), frames)
#a = frames[2].merge(frames[3], how='inner', suffixes=('x','y'), left_index=True, right_index=True)
#join fear_crime which is a Series object
b = a.join(fear_crime, how='inner')
all_data = b.join(Turnout, how='inner')
all_data = all_data.fillna(0)
all_data = all_data.rename(index=str, columns={31:'Fear Crime', u'2015Pay (£)':'2015 Pay'})
#check which boroughs dropped out
mayor_votes.index.difference(all_data.index)
#this is to group minor political parties and facilitate the analysis
all_data['Other Party'] = all_data[['Liberal Democrats', "All People's Party", 'Respect (George Galloway)', 'Take Back the City']].sum(axis=1)
#city of london drops out as a lot of datasets lack information for the borough
all_data.to_csv('projects/referendum votes/Worked data/all_data', encoding='utf-8', index_label='Borough')
