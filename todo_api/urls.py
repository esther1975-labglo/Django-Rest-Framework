
from django.urls import path, include
from rest_framework import routers
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
    SnippetHighlight,
    TodosList,
    filter_todoList,
    UserListView,
    ProductList
    #login_api

   
)
from todo_api import views
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'userr', views.Hyper_UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'SnippetViewSet', views.SnippetViewSet)
router.register(r'Hyper_SnippetViewSet', views.Hyper_SnippetViewSet, basename="snippet-highlight")


'''app_name = todo_api'''

urlpatterns = [
    #class based views
    path('register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('login/', views.LoginView.as_view()),
    path('ExampleView', ExampleView.as_view()),
    path('UserListView', UserListView.as_view()),
    path('api', TodoListApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('filter/', filter_todoList.as_view()),
    path('products', ProductListApiView.as_view()),
    path('ProductList', ProductList.as_view()),
    path('TodosList', TodosList.as_view()),
    path('product/<int:product_id>/', ProductDetailApiView.as_view()),
    path('SnippetList/<int:pk>/', SnippetList.as_view()),
    path('Snippet/<int:pk>/', SnippetDetail.as_view()),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
   

    #function based views
    path('', include(router.urls)),
    path('snippet_list', views.snippet_list, name = "snippet_list"),
    path('snippet_detail/<int:pk>', views.snippet_detail, name = "snippet_detail"),
    path('api_root', views.api_root, name = 'api_root'),
    path('Hyper_Snippet', views.Hyper_Snippet_list, name = "Snippet_Detail"),
    path('simple_html_view', views.simple_html_view, name = "simple_html_view"),
  


    

    
   
    
   
  
]