from django.contrib import admin
from django.urls import path,include
from Add_Update_Movies import views
# from django.conf import settings
# from django.conf.urls.static import static
urlpatterns = [

   
    path('addmovie/',views.Submit_Movie),
    path('update_status/<int:id>',views.Update_Movie_Status),

]
