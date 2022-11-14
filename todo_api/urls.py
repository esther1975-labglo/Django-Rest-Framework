#from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from . import views
from todo_api import views
from .views import (
    ExampleView,
    TodoListApiView,
    TodoDetailApiView,
    ProductListApiView,
    ProductDetailApiView,
    SnippetList,
    SnippetDetail,
    IsOwnerOrReadOnly,
    #login_api

   
)
from todo_api import views
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)




urlpatterns = [
    path('ExampleView', ExampleView.as_view()),
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('products', ProductListApiView.as_view()),
    path('product/<int:product_id>/', ProductDetailApiView.as_view()),
    path('SnippetList/<int:pk>/', SnippetList.as_view()),
    path('Snippet/<int:pk>/', SnippetDetail.as_view()),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('snippet_list', views.snippet_list, name = "snippet_list"),
    path('snippet_detail/<int:pk>', views.snippet_detail, name = "snippet_detail"),
    path('IsOwnerOrReadOnly', views.IsOwnerOrReadOnly, name = 'IsOwnerOrReadOnly'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('login/', views.LoginView.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    




    

    
   
    
   
  
]