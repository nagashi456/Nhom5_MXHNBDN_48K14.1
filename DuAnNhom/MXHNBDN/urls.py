from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
# path('', views.index, name='index'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('create-private-chat/', views.create_private_chat, name='create_private_chat'),
    path('create-group-chat/', views.create_group_chat, name='create_group_chat'),
    path('api/search-users/', views.search_users, name='search_users'),
    path('api/upload-attachment/', views.upload_attachment, name='upload_attachment'),
    path('binh_luan/', views.Binhluan, name='binhluan'),
    path('binh-chon/tao/', views.tao_binh_chon, name='tao_binh_chon'),
    path('binh-chon/', views.danh_sach_binh_chon, name='danh_sach_binh_chon'),
    ######################################################################
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('nhan_tin/', views.Nhantin, name='nhantin'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_detail/',views.ProfileDetail,name='profile_detail'),
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
    path('',views.trang_chu,name='trang_chu'),
    path('quen_pass/',views.Quenpass,name='Quenpass')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

