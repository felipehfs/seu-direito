from django.shortcuts import render
from django.shortcuts import redirect 
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


from .forms import UserForm
from .forms import AdvogadoForm
from .forms import EmpresaForm
from .forms import OrdemDeServicoForm
from .forms import PropostaForm
from .models import User, AdvogadoProfile, EmpresaProfile, OrdemDeServico, Proposta


class RegistrationView(FormView):
	""" Action responsável pelo cadastro de novos usuários """
	template_name = 'app/register.html'
	form_class = UserForm
	success_url = '/tanks/'

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.username = form.cleaned_data['username']
		obj.tipo = form.cleaned_data['tipo']
		
		obj.set_password(form.cleaned_data['password'])
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
	if request.user.tipo == 'a':
		propostas_aceitas = Proposta.objects.filter(advogado=request.user, aceito=True)
		print(propostas_aceitas)
		return render(request, 'app/sistema.html', {'aceitas': propostas_aceitas})
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


@login_required(login_url='app:index')
def novo_servico(request):
	if request.user.tipo == 'a': # se for um advogado ele redicionará para página original do sistema
		return redirect('app:sistema')
	elif request.method == 'POST':
		servico = OrdemDeServicoForm(request.POST)
		servico.instance.empresa = request.user 
		if servico.is_valid():
			servico.save()
			return redirect('app:sistema')
		return render(request, 'app/novo_servico.html', {'form': servico})

	servico = OrdemDeServicoForm()
	servico.instance.empresa = request.user 
	return render(request, 'app/novo_servico.html', {'form': servico})

@login_required(login_url='app:index')
def ordens_de_servico(request):
	if request.user.tipo == 'e':
		ordens = OrdemDeServico.objects.filter(empresa=request.user)
	else:
		ordens = OrdemDeServico.objects.filter(status="Criada")
	return render(request, 'app/ordem_servico.html', {'ordens': ordens})

@login_required(login_url='app:index')
def remove_ordem(request, ord_id):
	query = OrdemDeServico.objects.get(pk=ord_id)
	query.delete()
	return redirect('app:sistema')

@login_required(login_url='app:index')
def detalhes_ordem(request, ord_id):
	query = OrdemDeServico.objects.get(pk=ord_id)
	try:
		info_empresa = EmpresaProfile.objects.get(user=query.empresa)
	except EmpresaProfile.DoesNotExist:
		info_empresa = None
	proposta = Proposta.objects.filter(servico=query)
	return render(request, 'app/detalhes_servico.html', 
			{'ordem': query, 
				'propostas': proposta, 
				'info_empresa': info_empresa, 'advise': "Preencha suas informações pessoais" })

@login_required(login_url='app:index')
def enviar_proposta(request, ord_id):
	if request.method == 'GET':
		ordem = OrdemDeServico.objects.get(pk=ord_id)
		try:
			proposta = Proposta.objects.get(advogado=request.user, servico=ordem)
			form = PropostaForm(instance=proposta)
		except Proposta.DoesNotExist:
			form = PropostaForm()
		return render(request, 'app/nova_proposta.html',{'form': form})

	if request.method == 'POST':
		form = PropostaForm(request.POST)
		ordem = OrdemDeServico.objects.get(pk=ord_id)
		form.instance.servico = ordem
		form.instance.advogado = request.user
		if form.is_valid():
			form.save()
			return redirect('app:sistema')
		return render(request, 'app/nova_proposta', {'form': form})

@login_required(login_url='app:index')
def aceita_proposta(request, ord_id, prop_id):
	if request.user.tipo == 'a':
		return redirect('app:index')

	prop = Proposta.objects.get(pk=prop_id)
	prop.aceito = True 
	prop.save()

	servico = OrdemDeServico.objects.get(pk=ord_id)
	servico.status = 'Delegada'
	servico.save()
	return redirect('app:sistema')

@login_required(login_url='app:index')
def finaliza_ordem(request, ordem_id):
	if request.user.tipo == 'a':
		return redirect('app:index')

	ordem = OrdemDeServico.objects.get(pk=ordem_id)
	ordem.status = "Finalizada"
	ordem.save()
	return redirect('app:sistema')