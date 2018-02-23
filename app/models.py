from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, 
	UserManager)
from django.conf import settings 

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
	""" Classe que representa o profile do usuário """
	username = models.CharField('nome', max_length=30, unique=True)
	email = models.EmailField('E-mail', unique=True, max_length=30)
	tipo = models.CharField('categoria', choices=(('a', 'advogados'), ('e', 'empresas')), max_length=30)

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
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	telefone = models.CharField("Telefone",  max_length=20)
	cpf = models.CharField("CPF", max_length=20, unique=True)

	def __str__(self):
		return self.user.username