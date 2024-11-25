from django.contrib import admin
from django.urls import path
from words import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('words_list/', views.words_list, name='words_list'),
    path('add_word/', views.add_word, name='add_word'),
]
