from django.urls import path,include
from . import views
from knox.views import LogoutView
from knox import views as knox_views

urlpatterns = [
    path('',views.createBlog),
    path('getblog/<str:pk>',views.getBlog),
    path('savedBlog/',views.savedBlog),
    path('unSaveBlog/<str:blog_id>',views.unSaveBlog),
    path('deleteBlog/<str:blog_id>',views.deleteBlog),
    path('blogs/', views.SearchView.as_view()),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('currentuser/',views.current_user),
    path('deletetokens/',views.deletetokens),
    path('userBlog/',views.userBlog),
    path('otherUserBlog/',views.otherUserBlog),
    path('updateBlog/<str:pk>',views.updateBlog),
    path('changepassword/',views.changePassword),
    path('report/',views.reportBlog),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
