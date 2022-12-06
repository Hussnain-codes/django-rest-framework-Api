from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerUser),
    path('login', views.loginUser),
    path('user', views.userView),
    path('logout', views.logoutUser),
    path('createpost', views.createPost),
    path('post', views.getPosts),
]
