from django.urls import path
from . import views
urlpatterns = [
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('binh_chon/', views.BinhChon, name='binhchon'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('nhan_tin/', views.Nhantin, name='nhantin'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_detail/',views.ProfileDetail,name='profile_detail'),
    path('login/',views.DangNhap,name='dang_nhap'),
    path('trang_chu/',views.Trangchu,name='trang_chu')
]
