from django.urls import path
from .views import transfer_money

urlpatterns = [
     path('transfer/', transfer_money , name='transfer_money'),
  
]