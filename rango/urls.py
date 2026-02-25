from django.urls import path
from rango import views 

urlpatterns = [
    path('', views.index, name = 'index'), 
    path('about', views.about, name = 'about'),
    path('category/<slug:category_name_slug>', views.show_category, name = 'show_category'), #the book used an older method for capturing the parameters using regex but here i used a newer method 
]