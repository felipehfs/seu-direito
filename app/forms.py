from django import forms 
from .models import User, AdvogadoProfile 

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

class AdvogadoForm(forms.ModelForm):

	telefone = forms.RegexField(label='Telefone', max_length=20, regex=r'(\d{4,5})-(\d{4})')
	cpf = forms.RegexField(label='cpf', max_length=20, regex=r'(\d{3})\.(\d{3})\.(\d{3})-(\d{2})')
	user = forms.HiddenInput()

	def __init__(self, *args, **kwargs):
	
		super(AdvogadoForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
			
	class Meta:
		model = AdvogadoProfile
		fields = ['cpf', 'telefone']