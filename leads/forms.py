from django import forms
from .models import Lead,Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UsernameField

User=get_user_model()
class LeadModelForm(forms.ModelForm): # easier to work with model forms 
    class Meta:
        model=Lead
        fields=(
            'first_name','last_name','age','agent','description',
            'phone_number','email',
        )
    
class LeadForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    age=forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email")
        # field_classes = {'username': UsernameField}
class AssignAgentForm(forms.Form):
    agent=forms.ModelChoiceField(queryset=Agent.objects.none())
    
   # for dynamic display of agents
    def __init__(self, *args, **kwargs):
        request=kwargs.pop("request")
        agents=Agent.objects.filter(organisation=request.user.profile)
        super(AssignAgentForm,self).__init__(*args,**kwargs) # to instantiate the form
        self.fields["agent"].queryset=agents

class LeadCategoryUpdateForm(forms.ModelForm):
      class Meta:
        model=Lead
        fields=(
            'category',
        )
    
