from django import forms 
from .models import User 

class RegistrationForm(forms.ModelForm):
	password1 = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
	class Meta:
		model = User 
		fields = ['username', 'tipo', 'email']
