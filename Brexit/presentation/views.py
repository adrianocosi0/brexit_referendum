from django.shortcuts import render
import pandas as pd
from . import data_analysis
from django.http import HttpResponse
from . import forms

def index(request):
		#return webpage with empty form
		form = forms.Define_Variables_Form()
		return render(request, 'presentation/layout.html', {'form':form})
		
def graph(request):
	if request.method == 'POST':
		#get form data in the form
		form = forms.Define_Variables_Form(request.POST)
		#process data and pass it to the function
		if form.is_valid():
			data = form.cleaned_data
			arguments = data['arguments']
			area_variable = data['area_variable']
			fig = data_analysis.plot_bubbles(arguments, data_analysis.all_data[area_variable])
			response = HttpResponse(content_type='image/png')
			fig.savefig(response)
			return response
	else:
		parties = ["Conservative Party", "Labour Party", "Green Party", "UKIP"]
		fig = data_analysis.plot_bubbles(parties, data_analysis.all_data['2015 Pay'])
		response = HttpResponse(content_type='image/png')
		fig.savefig(response)
		return response
		# #user should not be here, template just gives a link to redirect to presentation page
		# return render(request, 'presentation/wrong_place.html')