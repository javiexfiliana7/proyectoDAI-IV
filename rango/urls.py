from django.conf.urls import patterns, url
from rango import views
from django.conf import settings # New Import
from django.conf.urls.static import static # New Import

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^tapa/(?P<tapa_name_slug>[\w\-]+)/$', views.tapa, name='tapa'),
    url(r'^add_tapa/$', views.add_tapa, name='add_tapa'), # NEW MAPPING
    url(r'^tapa/(?P<tapa_name_slug>\w+)/add_bar/$', views.add_bar, name='add_bar'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^tapa/(?P<tapa_name_slug>[\w\-]+)/bar/(?P<nombre_bar>[\w\-]+)/$',  views.bar, name="bares"),
    url(r'^datos/$', views.reclama_datos, name="reclama_datos"),)



if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
