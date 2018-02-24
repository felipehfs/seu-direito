from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings 

class User(AbstractBaseUser, PermissionsMixin):
	""" Classe que representa o profile do usuário """
	username = models.CharField('nome', max_length=30, unique=True)
	email = models.EmailField('E-mail', unique=True, max_length=30)
	tipo = models.CharField('categoria', choices=(('a', 'advogados'),
				('e', 'empresas')), max_length=30)

	is_staff = models.BooleanField('É da equipe?', default=False)
	is_active = models.BooleanField("Esta ativo?", default=True)
	data_joined = models.DateTimeField('Data de entrada', auto_now_add=True)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username 

	def get_short_name(self):
		return self.username 

	def get_full_name(self):
		return str(self)

	class Meta:
		verbose_name = "Usuário"
		verbose_name_plural = "Usuários"

class AdvogadoProfile(models.Model):
	""" AdvogadoProfile representa os dados pessoais do advogado """
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	telefone = models.CharField("Telefone",  max_length=20)
	cpf = models.CharField("CPF", max_length=20, unique=True)

	def __str__(self):
		return self.user.username

class EmpresaProfile(models.Model):
	""" EmpresaProfile representa os dados pessoais da empresa """
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ramo = models.CharField('Ramo de atuação', max_length=30)

	def __str__(self):
		return self.user.username


class OrdemDeServico(models.Model):
	""" OrdemDeServiço representa a oferta de trabalho das empresas """
	STATUS = (('CRIADA', 'Criada'), 
				('DELEGADA', 'Delegada'),
				('FINALIZADA', 'Finalizada'))

	empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	titulo =  models.CharField('Título',max_length=25)
	descricao = models.TextField('Descrição')
	status = models.CharField(max_length=30, choices=STATUS, default='Criada')

	def __str__(self):
		return self.empresa.username

class Proposta(models.Model):
	""" Proposta representa a oferta do advogado """
	advogado = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	valor = models.DecimalField('valor', max_digits=20, decimal_places=2)
	servico = models.ForeignKey(OrdemDeServico, on_delete=models.CASCADE)
	aceito = models.BooleanField(default=False)

	def __str__(self):
		return self.advogado.username