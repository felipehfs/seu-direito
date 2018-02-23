from django import forms 
from .models import User, AdvogadoProfile, EmpresaProfile

class UserForm(forms.ModelForm):
	""" UserForm representa a entidade usuário do sistema """
	password1 = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		""" adicionando estilo aos campos """
		super(UserForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
	class Meta:
		model = User 
		fields = ['username', 'tipo', 'email']

class AdvogadoForm(forms.ModelForm):
	""" """
	telefone = forms.RegexField(label='Telefone', max_length=20, regex=r'(\d{4,5})-(\d{4})')
	cpf = forms.RegexField(label='cpf', max_length=20, regex=r'(\d{3})\.(\d{3})\.(\d{3})-(\d{2})')
	user = forms.HiddenInput()

	def __init__(self, *args, **kwargs):
		""" adicionando estilo aos campos """
		super(AdvogadoForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
			
	class Meta:
		model = AdvogadoProfile
		fields = ['cpf', 'telefone']

class EmpresaForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		""" Adicionando setilo aos campos """
		super(EmpresaForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
	class Meta:
		model = EmpresaProfile
		fields = ['ramo']