#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import statsmodels.api as sm

all_data = pd.read_csv('projects/referendum votes/Worked data/all_data', index_col='Borough')

'''Leave votes by mayor votes. 
Scatterplots by political orientation (proxy is mayor votes election %)'''

orientations = ['Conservative Party', 'Labour Party', 'Green Party', 'UK Independence Party (UKIP)']

colors = np.random.rand(len(all_data.index))

area = []

def plot_bubbles(arguments, area_variable, space=0):

	ah = iter(arguments)

	eh = iter(arguments)

	ih = iter(arguments)

	kh = iter(arguments)

	th = iter(arguments)

	zh = iter(arguments)

	mh = iter(arguments)

	fig, axes = plt.subplots(2,2,figsize=(15,12))

	for x in area_variable:
		#want the bubbles to have an average area of 40, add a factor to increase the variability in size
		factor = ((x-area_variable.mean())**2/400)
		area.append(factor*x*(40/area_variable.mean()))

	for i in range(2):
		for j in range(2):
			orient = all_data[ah.next()]
			axes[i,j].set_ylabel('Leave %')
			axes[i,j].set_xlim([max(0, all_data[zh.next()].min()-all_data[mh.next()].min()/3),
			 all_data[ih.next()].max()+all_data[th.next()].max()/7])
			results = sm.OLS(all_data['Leave votes'], sm.add_constant(orient)).fit()
			X_plot = np.linspace(orient.min()-0.05, orient.max(), 100)
			axes[i,j].plot(X_plot, X_plot*results.params[1] + results.params[0], )
			# for label, ori, leave in zip(all_data.index, orient, all_data['Leave votes']):
			# 	axes[i,j].annotate(label, xy=(ori, leave), xytext=(ori, leave+0.1), 
			# 	arrowprops={'facecolor':'black', 'connectionstyle':'arc3,rad=0.3', 'arrowstyle':'simple'})
			axes[i,j].scatter(orient, all_data['Leave votes'], s=area, c=colors, alpha=0.6)
			if i == 0:
				axes[i,j].set_title(kh.next())
			if i == 1:
				axes[i,j].set_xlabel(kh.next())
	fig.subplots_adjust(hspace=space, wspace=space)
	fig.show()

plot_bubbles(orientations, all_data['2015 Pay'])

'''Leave votes by Fear of Crime and ethnicity'''

parties = ['Fear Crime', 'White', 'Asian', 'Black']

plot_bubbles(parties, all_data['% Turnout'])

plot_bubbles(orientations, all_data['% Turnout'])
