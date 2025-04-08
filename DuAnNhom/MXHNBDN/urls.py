from django.urls import path
from . import views
urlpatterns = [
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('',views.index,name='index'),
    path('profile_details/',views.detail_profile, name = 'profile_details'),

]
