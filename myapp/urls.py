from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myapp'
urlpatterns = [
    # ex: /myapp/
    url(r'^$', views.index, name='index'),
    url(r'^prosilci', views.aktiviraj, name='aktiviraj_prosilce'),
    url(r'^uporabniki/potrdi/(?P<username>[\-\w]+)/$', views.potrdi, name='potrdi'),
    url(r'^uporabniki/spremeni/(?P<username>[\-\w]+)/$', views.spremeni, name='spremeni_nadzornike'),
    url(r'^stran/dodaj/$', views.dodajStran, name='dodaj_stran'),
    url(r'^stran/uredi/(?P<stran_id>[0-9]+)/$', views.uredi, name='uredi'),
    url(r'^stran/izbrisi/(?P<pk>[0-9]+)/$', views.IzbrisiStranView.as_view(), name='izbrisi'),
    url(r'^stran/(?P<stran_id>[0-9]+)/$', views.stran, name='stran'),
    url(r'^login/$', auth_views.login, {'template_name': 'myapp/login.html', 'extra_context': {'next': '/myapp'}}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/myapp'}, name='logout'),
    url(r'^registracija/$', views.registracija, name='registracija'),
    url(r'^profil/(?P<username>[\-\w]+)/$', views.profil, name='profil'),
    url(r'^profil/password/change/$', auth_views.password_change,  {'template_name': 'myapp/profil.html', 'post_change_redirect': 'myapp:logout'}, name='password-change'),
]