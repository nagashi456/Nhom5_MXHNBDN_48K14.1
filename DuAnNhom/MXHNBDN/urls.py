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
    path('binh_chon/', views.tao_binh_chon, name='binhchon'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('nhan_tin/', views.Nhantin, name='nhantin'),
    path('tao_tai_khoan/',views.TaoTaiKhoan,name='tao_tai_khoan'),
    path('profile_detail/',views.ProfileDetail,name='profile_detail'),
path('binh_chon/<int:pk>/', views.chi_tiet_binh_chon, name='chi-tiet-binh-chon'),

    # path('login/',views.DangNhap,name='dang_nhap'),
    path('', views.Trangchu, name='trang_chu'),

    path('login/',views.login_view,name='dang_nhap'),
    path('logout/', views.logout_view, name='logout'),
    path('',views.Trangchu,name='trang_chu'),
    path('quen_pass/',views.Quenpass,name='Quenpass')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

