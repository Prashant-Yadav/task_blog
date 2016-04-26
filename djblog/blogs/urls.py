from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add_blog/$', views.add_blog, name='add_blog'),
    url(r'^blog_view/(?P<blog_id>[0-9]+)/$', views.blog_view, name='blog_view'),
    url(r'^edit_blog/(?P<blog_id>[0-9]+)/$', views.edit_blog, name='edit_blog'),
    url(r'^delete_blog/(?P<blog_id>[0-9]+)/$', views.delete_blog, name='delete_blog'),
]
