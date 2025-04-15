from django.urls import path
from . import views
urlpatterns = [
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('binh_chon/', views.BinhChon, name='binhchon'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('nhan_tin/', views.Nhantin, name='nhantin'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_detail/',views.ProfileDetail,name='profile_detail'),
    path('login/',views.login_view,name='dang_nhap'),
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
]
