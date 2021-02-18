from django.contrib import admin
from django.urls import path,include
from .views import (LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,
LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategoryUpdateView)

urlpatterns = [
    path('',LeadListView.as_view(),name='lead_list'),
    path('<int:pk>/',LeadDetailView.as_view(),name='lead_detail'), #syntax for primary key in route
    path('<int:pk>/update/',LeadUpdateView.as_view(),name='lead_update'),
    path('<int:pk>/delete/',LeadDeleteView.as_view(),name='lead_delete'),
    path('create/',LeadCreateView.as_view(),name='lead_create'), #syntax for primary key in route
    path('<int:pk>/assign_agent/',AssignAgentView.as_view(),name='assign_agent'),
    path('<int:pk>/category/',LeadCategoryUpdateView.as_view(),name='lead_category_update'),
    path('categories/',CategoryListView.as_view(),name='category_list'), 
    path('categories/<int:pk>/',CategoryDetailView.as_view(),name='category_detail'), 
]

app_name='leads'