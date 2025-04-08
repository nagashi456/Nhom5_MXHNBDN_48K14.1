from django.contrib import admin
from .models import (
    NguoiDung, VaiTro,
    BaiViet, BinhLuan,
    CuocTroChuyen, TinNhan,
    BinhChon, LuaChonBinhChon, BinhChonNguoiDung,
    Nhom, ThanhVienNhom,

)
from django.contrib.auth.admin import UserAdmin

@admin.register(NguoiDung)
class NguoiDungAdmin(UserAdmin):
    model = NguoiDung
    list_display = ('username', 'email', 'so_dien_thoai', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email', 'so_dien_thoai')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ("Thông tin bổ sung", {
            "fields": ("so_dien_thoai", "avatar"),
        }),
    )

admin.site.register(VaiTro)

@admin.register(BaiViet)
class BaiVietAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'ngay_tao')
    search_fields = ('noi_dung',)

@admin.register(BinhLuan)
class BinhLuanAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'bai_viet', 'ngay_tao')
    search_fields = ('noi_dung',)

@admin.register(CuocTroChuyen)
class CuocTroChuyenAdmin(admin.ModelAdmin):
    list_display = ('id', 'ten_nhom')
    filter_horizontal = ('thanh_vien',)

@admin.register(TinNhan)
class TinNhanAdmin(admin.ModelAdmin):
    list_display = ('nguoi_gui', 'cuoc_tro_chuyen', 'ngay_tao')
    search_fields = ('noi_dung',)

@admin.register(BinhChon)
class BinhChonAdmin(admin.ModelAdmin):
    list_display = ('ten_tieu_de', 'nguoi_tao', 'thoi_gian_ket_thuc')
    search_fields = ('ten_tieu_de',)

@admin.register(LuaChonBinhChon)
class LuaChonBinhChonAdmin(admin.ModelAdmin):
    list_display = ('binh_chon', 'noi_dung')

@admin.register(BinhChonNguoiDung)
class BinhChonNguoiDungAdmin(admin.ModelAdmin):
    list_display = ('nguoi_dung', 'lua_chon')

@admin.register(Nhom)
class NhomAdmin(admin.ModelAdmin):
    list_display = ('ten_nhom', 'ngay_tao')

@admin.register(ThanhVienNhom)
class ThanhVienNhomAdmin(admin.ModelAdmin):
    list_display = ('nhom', 'nguoi_dung', 'ngay_gia_nhap')



# Register your models here.

# Register your models here.
