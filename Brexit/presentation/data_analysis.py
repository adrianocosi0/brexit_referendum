#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pylab import figure, axes, plot, title, subplots
import statsmodels.api as sm
from sqlalchemy import create_engine
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib

# Load data from database into dataframe

engine = create_engine("postgresql://user_name:password@localhost:5432/postgres")

all_data = pd.read_sql('''SELECT * FROM records;''', engine, index_col='Borough')

# Bubble Plot function creation

colors = np.random.rand(len(all_data.index))

def plot_bubbles(arguments, area_variable, name, space=0.1):

	ah = iter(arguments)

	eh = iter(arguments)

	ih = iter(arguments)

	kh = iter(arguments)

	th = iter(arguments)

	zh = iter(arguments)

	mh = iter(arguments)

	fig = figure(figsize=(30, 25))

	ax1 = fig.add_subplot(2,2,1)

	ax2 = fig.add_subplot(2,2,2)

	ax3 = fig.add_subplot(2,2,3)

	ax4 = fig.add_subplot(2,2,4)

	collection = [ax1, ax2, ax3, ax4]

	'''want the bubbles to have an average area of 20**2.8. standardize variable and multiply it 
    by a factor 20**2.65 to increase the variability in size'''
	area = [max(20**2.8 + ((x-area_variable.mean())/area_variable.std())*20**2.65, 5) for x in area_variable]
	for ax in collection:
		orient = all_data[ah.next()]
		ax.set_ylabel('Leave %')
		ax.set_xlim([max(0, all_data[zh.next()].min()-all_data[mh.next()].min()/3),
		 all_data[ih.next()].max()+all_data[th.next()].max()/7])
		results = sm.OLS(all_data['Leave votes'], sm.add_constant(orient)).fit()
		X_plot = np.linspace(orient.min()-0.05, orient.max(), 100)
		ax.plot(X_plot, X_plot*results.params[1] + results.params[0], )
		for label, ori, leave in zip(all_data.index, orient, all_data['Leave votes']):
			ax.annotate(label, xy=(ori, leave), xytext=(ori, leave+0.05), 
			arrowprops={'facecolor':'black', 'connectionstyle':'arc3,rad=0.3', 'arrowstyle':'simple'})
		ax.scatter(orient, all_data['Leave votes'], s=area, c=colors, alpha=0.6)
		ax.set_title(kh.next())
		if name:
			fig.suptitle("Bubble plot of Leave votes % by {}, bubble areas' variable is {}".format(name, area_variable.name), 
                     y=0.935, fontsize=20)
	return fig
