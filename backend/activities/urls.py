from django.urls import path
from .views import ActivityListCreateView,ActivityRetrieveUpdateDestroyView

urlpatterns =[
    path('',ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/',ActivityRetrieveUpdateDestroyView.as_view(), name='activity-list-deatail'),

]
