from django import forms
from . models import *

class NotesForm(forms.ModelForm):
    class Meta:
        # Binding Notes model to forms
        model = Notes
        fields = ['title', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


# Form to create homeworks
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        forms.widgets = {'due':DateInput()}
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        

# Youtube Search Form
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search : ")
    
    
# Todo Form
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'is_finished']
        
        
# Converter Form
class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'),('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    
    
# Length Converter Form
class ConversionLengthForm(forms.Form):
    CHOICES = [('yard', 'Yard'),('foot', 'Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {
            'type' : 'number',
            'placeholder' : 'Enter the Number'
        }
    ))
    measure1 = forms.CharField(
        label = '', widget=forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '', widget=forms.Select(choices = CHOICES)
    )
    
# Mass Converter Form
class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'),('kilogram', 'Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs = {
            'type' : 'number',
            'placeholder' : 'Enter the Number'
        }
    ))
    measure1 = forms.CharField(
        label = '', widget=forms.Select(choices = CHOICES)
    )
    measure2 = forms.CharField(
        label = '', widget=forms.Select(choices = CHOICES)
    )
    