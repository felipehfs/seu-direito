from django import forms 

from .models import User
from .models import AdvogadoProfile
from .models import EmpresaProfile
from .models import OrdemDeServico
from .models import Proposta


class UserForm(forms.ModelForm):
	""" UserForm representa a entidade usuário do sistema """
	password = forms.CharField(widget=forms.PasswordInput)

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
	""" AdvogadoForm representa o formulário sobre informações pessoais do advogado """
	telefone = forms.RegexField(label='Telefone', max_length=20, regex=r'(\d{4,5})-(\d{4})')
	cpf = forms.RegexField(label='cpf', max_length=20, 
		regex=r'(\d{3})\.(\d{3})\.(\d{3})-(\d{2})')
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
	""" EmpresaForm representa o formulário de informacões adicionais da empresa """
	def __init__(self, *args, **kwargs):
		""" Adicionando etilo aos campos """
		super(EmpresaForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		model = EmpresaProfile
		fields = ['ramo']

class OrdemDeServicoForm(forms.ModelForm):
	""" OrdemDeServicoForm representa o formulário da ordem de serviço """
	def __init__(self, *args, **kwargs):
		super(OrdemDeServicoForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})

	class Meta:
		model = OrdemDeServico
		fields = ['titulo', 'descricao']

class PropostaForm(forms.ModelForm):
	""" PropostaForm representa o formulário da proposta """
	def __init__(self, *args, **kwargs):
		super(PropostaForm, self).__init__(*args, **kwargs)
		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'
				})
	class Meta:
		model = Proposta
		fields = ['valor']