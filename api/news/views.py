from django.shortcuts import render
from rest_framework.generics import   ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import News
from .serializer import NewsCreateSerializer    # UserProfileChangeSerializer
from api.accounts.models import User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class NewsCreateNewsApiView(CreateAPIView):
    
    permission_classes = [IsAuthenticated, ]
    queryset= News.objects.all()
    serializer_class = NewsCreateSerializer
    
    
class NewsListApiView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset= News.objects.all()
    serializer_class = NewsCreateSerializer    
    
class NewsUpdateView(RetrieveAPIView):
    
    permission_classes = [IsAuthenticated, ]
    queryset= News.objects.all()
    serializer_class = NewsCreateSerializer
    
class NewsRetrivView(UpdateAPIView):
    
    # permission_classes = [AllowAny, ]
    # # queryset= News.objects.all()
    # serializer_class = NewsCreateSerializer
    
    # def get_queryset(self):
    #     queryset =News.objects.filter(author = self.request.user, id=self.kwargs['pk'])
    #     return queryset
    
    # def update(self, request,*args, **kwargs):
    #     instance =self.get_object()
    #     if not instance:
    #         return Response('cannot daleted', status=status.HTTP_400_BAD_REQUEST)
    #     self.perform_update()
    
    
    permission_classes = (IsAuthenticated, )
   
    serializer_class = NewsCreateSerializer


    def get_queryset(self):
        queryset = News.objects.filter(user = self.request.user, id = self.kwargs['pk'])
        return queryset
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not  instance :
            return Response("Cannot update NEWS", status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(instance)
        
        data ={
            'message':'news is updated'
            
        }
        return Response(data)

    
    
    
class DeleteLedgerCategory(DestroyAPIView):
    serializer_class = NewsCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = News.objects.filter(author = self.request.user, id=self.kwargs['pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not  instance :
            return Response("Cannot delete NEWS", status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        
        data ={
            'message':'news is daleted'
            
        }
        return Response(data)
    
    


# from rest_framework import generics, mixins, permissions

# # User = get_user_model()

# class UserIsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.id == request.user.id

# class UserProfileChangeAPIView(generics.RetrieveAPIView,
#                                mixins.DestroyModelMixin,
#                                mixins.UpdateModelMixin):
#     permission_classes = (
#         permissions.IsAuthenticated,
#         UserIsOwnerOrReadOnly,
#     )
#     serializer_class = UserProfileChangeSerializer
#     parser_classes = (MultiPartParser, FormParser,)

#     def get_object(self):
#         username = self.kwargs["username"]
#         obj = get_object_or_404(User, username=username)
#         return obj

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    

    
    
    
