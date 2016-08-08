from django import forms

choices_arguments = (
	(["Conservative Party", "Labour Party", "Green Party", "UKIP"], 'Parties'), 
			(["White", "Black", "Asian", "Mixed"], 'Ethnicity'), 
			(["Turnout", "2015 Pay", "Fear Crime", "Other Party"],'Stats'), 
)
choices_area = (
	("2015 Pay", 'Earning'), 
	('Turnout', 'Turnout'), 
	('Fear Crime', 'Fear of Crime'),
)

class Define_Variables_Form(forms.Form):
	arguments = forms.TypedChoiceField(choices_arguments)
	area_variable = forms.TypedChoiceField(choices_area)
