"""djangologin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
import djangologin.dash_app_code as dd
import djangologin.outros as outros
import djangologin.financeiro as financ

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('vendas/', dd.graficos_vendas, name='vendas'),
    #path('vendas/', TemplateView.as_view(template_name='vendas.html'), name='vendas'),
    #path('financeiro/', financ.graficos_financ, name='financeiro'),
    path('financeiro/', TemplateView.as_view(template_name='financeiro.html'), name='financeiro'),
    #path('markerting/', TemplateView.as_view(template_name='markerting.html'), name='markerting'),
    path('outros/', TemplateView.as_view(template_name='outros.html'), name='outros'),
    path('outros_plot/', include('django_plotly_dash.urls')),
    #path(r'core/', include('core.models')),

]

admin.site.site_header = "Administração do Site Analytics"
admin.site.site_title = "Analytics - OPE"
admin.site.index_title = "Configurações"
