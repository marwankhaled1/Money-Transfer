from django.urls import path
from .views import AccountDetailView,upload_file,AccountListView

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('', AccountListView.as_view(), name='account_list'),
    path('<str:pk>/', AccountDetailView.as_view(), name='account_detail'),
   
]