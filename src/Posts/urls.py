from django.conf.urls import url

from . import views as postViews

urlpatterns = [
    url(r'^$', postViews.postsHomeView, name="all_posts"), #need to have a home view to handle '/posts'
    url(r'^create/$', postViews.postsCreateView, name="create_post"),
    url(r'^(?P<id>\d+)/$', postViews.singlePostView, name="single_post"),
    url(r'^(?P<id>\d+)/edit/$', postViews.singlePostEditView, name="edit_single_post"),
    url(r'^(?P<id>\d+)/delete/$', postViews.postsDeleteView),
]