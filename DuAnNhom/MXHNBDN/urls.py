from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
# path('', views.index, name='index'),
path('chat/', views.index, name='nhantin'),
    path('api/rooms/', views.room_list, name='room_list'),
    path('api/rooms/<int:room_id>/messages/', views.room_messages, name='room_messages'),
    path('api/rooms/create_private/', views.create_private_room, name='create_private_room'),
    path('api/users/search/', views.search_users, name='search_users'),
    path('api/users/current/', views.current_user, name='current_user'),
    path('api/upload/file/', views.upload_file, name='upload_file'),
    path('api/upload/image/', views.upload_image, name='upload_image'),
    path('binh_luan/', views.Binhluan, name='binhluan'),
    # path('binh_chon/', views.tao_binh_chon, name='binhchon'),
    path('binh-chon/tao/', views.tao_binh_chon, name='tao_binh_chon'),
    path('binh-chon/', views.danh_sach_binh_chon, name='danh_sach_binh_chon'),
    ######################################################################
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_view/',views.ProfileDetail,name='profile_view'),
    path('tao_bai_viet/', views.tao_bai_viet, name='tao_bai_viet'),
    path('bai-viet/sua/<int:bai_viet_id>/', views.sua_bai_viet, name='sua_bai_viet'),
    path('bai-viet/xoa/<int:bai_viet_id>/', views.xoa_bai_viet, name='xoa_bai_viet'),
    path('binh-chon/sua/<int:binh_chon_id>/', views.sua_binh_chon, name='sua_binh_chon'),
    path('binh-chon/xoa/<int:binh_chon_id>/', views.xoa_binh_chon, name='xoa_binh_chon'),
    path('', views.trang_chu, name='trang_chu'),
    path('them-binh-luan/<int:bai_viet_id>/', views.them_binh_luan, name='them_binh_luan'),
    path('xu-ly-cam-xuc/', views.xu_ly_cam_xuc, name='xu_ly_cam_xuc'),
    path('xu-ly-binh-chon/', views.xu_ly_binh_chon, name='xu_ly_binh_chon'),
    path('login/',views.login_view,name='dang_nhap'),
    path('logout/', views.logout_view, name='logout'),
    path('quen_pass/',views.Quenpass,name='Quenpass'),
    path('hoi-dap/', views.danh_sach_cau_hoi, name='danh_sach_cau_hoi'),
    path('cau-hoi/<int:cau_hoi_id>/', views.chi_tiet_cau_hoi, name='chi_tiet_cau_hoi'),
    path('tao-cau-hoi/', views.tao_cau_hoi, name='tao_cau_hoi'),
    path('sua-cau-hoi/<int:cau_hoi_id>/', views.sua_cau_hoi, name='sua_cau_hoi'),
    path('xoa-cau-hoi/<int:cau_hoi_id>/', views.xoa_cau_hoi, name='xoa_cau_hoi'),
    path('them-cau-tra-loi/<int:cau_hoi_id>/', views.them_cau_tra_loi, name='them_cau_tra_loi'),
    path('sua-cau-tra-loi/<int:cau_tra_loi_id>/', views.sua_cau_tra_loi, name='sua_cau_tra_loi'),
    path('xoa-cau-tra-loi/<int:cau_tra_loi_id>/', views.xoa_cau_tra_loi, name='xoa_cau_tra_loi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

