from django.shortcuts import render
import pandas as pd
from . import data_analysis
from django.http import HttpResponse
from . import forms
import ast
import matplotlib

#changing the backend to agg allows for threading
matplotlib.use('agg')

def index(request):
		#return webpage with empty form and first plot
		form = forms.Define_Variables_Form()
		return render(request, 'presentation/layout.html', {'form':form})
		
def graph(request):
	if request.method == 'POST':
		#get form data in the form
		form = forms.Define_Variables_Form(request.POST)
		#process data and pass it to the function
		if form.is_valid():
			data = form.cleaned_data
			arguments = ast.literal_eval(data['arguments'])
			area_variable = data['area_variable']
			for x in forms.choices_arguments:
				if arguments in x:
					name = x[1]
					fig = data_analysis.plot_bubbles(arguments, data_analysis.all_data[area_variable], name)
					response = HttpResponse(content_type='image/png')
					fig.savefig(response)
					return response

	else:
		parties = ["Conservative Party", "Labour Party", "Green Party", "UKIP"]
		fig = data_analysis.plot_bubbles(parties, data_analysis.all_data['2015 Pay'], 'parties')
		response = HttpResponse(content_type='image/png')
		fig.savefig(response)
		return response
		# #user should not be here, template just gives a link to redirect to presentation page
		# return render(request, 'presentation/wrong_place.html')
