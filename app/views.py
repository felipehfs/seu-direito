from django.shortcuts import render
from django.shortcuts import redirect 
from django.views.generic.edit import FormView
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

class RegistrationView(FormView):
	""" Action responsável pelo cadastro de novos usuários """
	template_name = 'app/register.html'
	form_class = RegistrationForm
	success_url = '/tanks/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.username = form.cleaned_data['username']
		obj.tipo = form.cleaned_data['tipo']
		
		obj.set_password(form.cleaned_data['password1'])
		obj.save()
		
		return HttpResponse("Salvo!")

def index(request):
	""" Home page com os campos de login """
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			print(form.get_user())
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