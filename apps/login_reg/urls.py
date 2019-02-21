from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login_reg_index"),
    url(r'^login_registration$', views.index, name="login_reg_index"),
    url(r'^get_login_page/', views.get_login_page, name="get_login_page"),
    url(r'^get_registration_page/', views.get_registration_page, name="get_registration_page"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^success$', views.success, name="success"),
    url(r'^logout$', views.logout, name="logout"),
]