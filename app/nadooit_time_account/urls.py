from django.urls import path
from . import views

# This is where the urls are placed
urlpatterns = [
    path("admin", views.admin, name="adminpage"),

]
