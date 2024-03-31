from django.contrib import admin
from django.urls import path
from Movies_Apis import views

urlpatterns = [

    path('',views.home_page),
    path('get_movie_api/',views.Movie_Api.as_view()),
    path('get_movie_api/<int:id>/',views.Movie_Api.as_view())

]