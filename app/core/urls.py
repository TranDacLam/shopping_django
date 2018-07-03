from django.conf.urls import url 
 
from . import views 

urlpatterns = [ 
    url(r'^$', views.home, name='home'),
    url(r'^products/$', views.products, name='products'),
    url(r'^product/detail/(?P<id>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^product/rating/$', views.product_rating, name='product_rating'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^cart/add/$', views.cart_add, name='cart_add'),
]