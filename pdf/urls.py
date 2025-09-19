from django.contrib import admin
from django.urls import path,include
from pdf import views

urlpatterns = [
    path('',views.landing,name='landing'),
    path('upload/',views.upload,name='upload'),
    path('analyze/', views.analyze, name='analyze'),
]
