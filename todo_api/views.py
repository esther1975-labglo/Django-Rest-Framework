from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import views
from todo_api.models import Todos, Snippets, Product
from todo_api.serializers import SnippetSerializer, ProductSerializer, TodoSerializer, UserSerializer, GroupSerializer, LoginSerializer
from rest_framework import mixins
from rest_framework import generics
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
#from pygments import highlight
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from pygments import highlight
from pygments.lexers import PythonLexer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authentication import TokenAuthentication


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        token = Token.objects.get_or_create(user=request.user)
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth), 
            'token': str(token) # None
        }
        return Response(content)


class TodoListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
       
        todos = Todos.objects.filter(user = request.user.id)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
      
        try:
            return Todos.objects.get(id=todo_id, user = user_id)
        except Todos.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class UserViewSet(viewsets.ModelViewSet):
   
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]







class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def save(self, *args, **kwargs):
   
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                              full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

@api_view(['GET', 'POST'])
def snippet_list(request):
   
    if request.method == 'GET':
        snippets = Snippets.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        serializer = SnippetSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippets.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippets.objects.all()
    serializer_class = SnippetSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user




@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippets.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

'''class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        print(snippet)
        lexer = get_lexer_by_name(snippet.language) 
        formatter = HtmlFormatter(linenos=snippet,
                              full=True)
        #self.highlighted = highlight(self.get_object()) 
        self.highlighted = highlight(snippet.code, lexer, formatter) 
        super(Snippet, self).save(*args, **kwargs) '''

'''from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer
from django.conf.auth import login

@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email
        },
        'token':token
    })

def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info':{
                'id':user.id,
                'username':user.username,
                'email':user.email
            },
        })
    return Response({'error':'not authenticated'}, status = 400)

@api_view(['POST']) 
def register_api(request):
    serializer = RegisterSerializer(data = request.data)
    serializer.is_valid(raise_exception = True) 

    user = serializer.save()
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_info':{
            'id':user.id,
            'username':user.username,
            'email':user.email
        },
        'token':token
    })  '''


''' Register'''

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token,created=Token.objects.get_or_create(user=user)
        return Response({
        "token": token.key,    
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)

'''login knox authentication'''

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

'''login authentication'''


class LoginView(views.APIView):
    
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        #token = Token.objects.get(user=user)
        #return Response({'token': token.key} ,status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_200_OK)
        #return Response(None)
        #return super(LoginView, self).post(request, format=None)

class ProductListApiView(APIView):
 
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
       
        products = Product.objects.filter(user = request.user.id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        
        data = {
            'title': request.data.get('title'), 
            'name': request.data.get('name'), 
            'price': request.data.get('price')
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailApiView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, product_id, user_id):
      
        try:
            return Product.objects.get(id=product_id)
        except Todos.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, product_id, *args, **kwargs):
        
        product_instance = self.get_object(product_id, request.user.id)
        if not product_instance:
            return Response(
                {"res": "Object with product id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(product_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, product_id, *args, **kwargs):
        
        product_instance = self.get_object(product_id, request.user.id)
        if not product_instance:
            return Response(
                {"res": "Object with product id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'), 
            'name': request.data.get('name'), 
            'price': request.data.get('price')
        }
        serializer = ProductSerializer(instance = product_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, product_id, *args, **kwargs):
        
        product_instance = self.get_object(product_id, request.user.id)
        if not product_instance:
            return Response(
                {"res": "Object with product id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        product_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )




def get_user_token(self, obj):
    return Token.objects.get_or_create(user=obj)[0].key



      

