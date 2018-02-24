from django.urls import path 

from . import views 

app_name = 'app'

urlpatterns = [
	path('', views.index, name="index"),
	path('registrar', views.RegistrationView.as_view(), name="registrar"),
	path('sistema', views.sistema, name="sistema"),
	path('sistema/profile', views.profile, name='profile'),
	path('sistema/empresas/servico/novo', views.novo_servico, name='novo_servico'),
	path('sistema/empresas/servicos', views.ordens_de_servico, name="ordem_de_servico"),
	path('logout', views.logout_user, name='logout'),
	path('sistema/empresas/servicos/<int:ord_id>', views.detalhes_ordem, name='detalhes_ordem'),
	path('sistema/empresas/servicos/<int:ord_id>/remove', views.remove_ordem, name='remove_ordem'),
	path('sistema/servicos/<int:ord_id>/proposta', views.enviar_proposta, name="enviar_proposta"),
]