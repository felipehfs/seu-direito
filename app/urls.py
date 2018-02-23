from django.urls import path 

from . import views 

app_name = 'app'

urlpatterns = [
	path('', views.index, name="index"),
	path('registrar', views.RegistrationView.as_view(), name="registrar"),
	path('sistema', views.sistema, name="sistema"),
	path('logout', views.logout_user, name='logout'),
]