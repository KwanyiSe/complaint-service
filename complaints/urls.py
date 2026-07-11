from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.complaint_form, name='complaint_form'),
    path('payment/<int:complaint_id>/', views.payment, name='payment'),
    path('status/<int:complaint_id>/', views.status, name='status'),
    path('track/', views.track_complaint, name='track'),
]