from django.urls import path
from .views import NewsCreateNewsApiView,  NewsListApiView,  NewsUpdateView, NewsRetrivView, DeleteLedgerCategory
from .models import News



urlpatterns =[
    path('create_news/', NewsCreateNewsApiView.as_view()),
    path('list_news/', NewsListApiView.as_view()),
    path('news_update/<int:pk>/', NewsUpdateView.as_view()),
    path('news_read/<int:pk>/', NewsRetrivView.as_view()),
    path('news_delete/<int:pk>/', DeleteLedgerCategory.as_view()),
] 