from django.urls import path
from . import views
urlpatterns = [
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('binh_chon/', views.tao_binh_chon, name='binhchon'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('nhan_tin/', views.Nhantin, name='nhantin'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_detail/',views.ProfileDetail,name='profile_detail'),
path('binh_chon/<int:pk>/', views.chi_tiet_binh_chon, name='chi-tiet-binh-chon'),

    # path('login/',views.DangNhap,name='dang_nhap'),
    path('', views.Trangchu, name='trang_chu'),
    path('tao_bai_viet/', views.TaoBaiViet, name='tao_bv'),
    path('sua_bai_viet/', views.SuaBaiViet, name='sua_bv'),
    path('login/',views.login_view,name='dang_nhap'),
    path('logout/', views.logout_view, name='logout'),
    # path('trang_chu/',views.Trangchu,name='trang_chu'),
    path('quen_pass/',views.Quenpass,name='Quenpass')
]
