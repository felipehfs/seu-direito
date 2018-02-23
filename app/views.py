from django.shortcuts import render
from django.shortcuts import redirect 
from django.views.generic.edit import FormView
from django.http import HttpResponse
from .forms import UserForm, AdvogadoForm, EmpresaForm
from .models import User, AdvogadoProfile, EmpresaProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

class RegistrationView(FormView):
	""" Action responsável pelo cadastro de novos usuários """
	template_name = 'app/register.html'
	form_class = UserForm
	success_url = '/tanks/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.username = form.cleaned_data['username']
		obj.tipo = form.cleaned_data['tipo']
		
		obj.set_password(form.cleaned_data['password1'])
		obj.save()
		login(self.request, obj)
		return redirect('app:sistema')

def index(request):
	""" Home page com os campos de login """
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return redirect('app:sistema')
		else:
			return render(request, 'app/index.html', {'form': form})
	return render(request, 'app/index.html', {'form': AuthenticationForm()})
	
def logout_user(request):
	logout(request)
	return redirect('app:index')

@login_required(login_url='app:index')
def sistema(request):
	return render(request, 'app/sistema.html', {})



@login_required(login_url='app:index')
def profile(request):
	# se o usuário for advogado a view redirecionará para o profile correto
	if request.method == 'GET':
		if request.user.tipo == 'a': # Exibindo as informações pessoais do profile de advogados
			try:
				advogado = AdvogadoProfile.objects.get(user=request.user)
				form = AdvogadoForm(instance=advogado)
			except AdvogadoProfile.DoesNotExist:
				form =  AdvogadoForm()
				form.instance.user = request.user

			return render(request, 'app/new_profile.html', {'form': form })

		if request.user.tipo == 'e': # Exibindo as informações pessoais do profile da empresa
			try:
				empresa = EmpresaProfile.objects.get(user=request.user)
				form = 	EmpresaForm(instance=empresa)
			except EmpresaProfile.DoesNotExist:
				form = EmpresaForm()
				form.instance.user = request.user 
			
			return render(request, 'app/new_profile.html', {'form': form})


	if request.method == 'POST':
		if request.user.tipo == 'a': # Atualizando ou salvando as informações pessoais do advogado
			try:
				advogado = AdvogadoProfile.objects.get(user=request.user)	
				form = AdvogadoForm(instance=advogado, data=request.POST)
			except AdvogadoProfile.DoesNotExist:
				form = AdvogadoForm(request.POST)
				form.instance.user = request.user 

			if form.is_valid():
				form.instance.user = request.user
				form.save()
				return redirect('app:sistema')
			return render(request, 'app/new_profile.html', {'form': form})

		if request.user.tipo == 'e':
			try:
				empresa = EmpresaProfile.objects.get(user=request.user)
				form =  EmpresaForm(instance=empresa, data=request.POST)
			except EmpresaProfile.DoesNotExist:
				form = EmpresaForm(request.POST)
				form.instance.user = request.user 

			if form.is_valid():
				form.save()
				return redirect('app:sistema')
			return render(request, 'app/new_profile.html', {'form': form})