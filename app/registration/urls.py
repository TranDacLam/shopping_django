from django.conf.urls import url 
 
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [ 
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/change_password/$', views.change_password, name='change_password'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        views.confirm_activation, name='confirm-activation'),
   	url(r'^password_reset/$', auth_views.password_reset, {"html_email_template_name": "registration/password_reset_email.html",
                                                          "email_template_name": "registration/password_reset_email.html"}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
]