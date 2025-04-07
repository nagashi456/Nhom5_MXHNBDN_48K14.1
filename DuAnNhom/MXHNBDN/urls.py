from django.urls import path
from . import views
urlpatterns = [
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
