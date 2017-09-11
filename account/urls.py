from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout, logout_then_login, password_change, password_change_done


urlpatterns = [
    # url(r'^login/$', views.user_login, name='login')
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'template_name': 'registration/log_out.html'}, name='logout'),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password-change/$', password_change, {'post_change_redirect':'account:password_change_done'}, name='password_change'),
    url(r'^password-change/done/$', password_change_done, name='password_change_done'),
]