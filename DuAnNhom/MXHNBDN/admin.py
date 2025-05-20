from django.contrib import admin
from . import models

@admin.register(models.PhongBan)
class PhongBanAdmin(admin.ModelAdmin):
    list_display = ('id', 'TenPhong', 'HinhAnhPhong')
    search_fields = ('TenPhong',)

@admin.register(models.NguoiDung)
class NguoiDungAdmin(admin.ModelAdmin):
    list_display = ('id', 'HoTen', 'SoDienThoai', 'Email', 'MaPhong', 'user')
    list_filter = ('MaPhong',)
    search_fields = ('HoTen', 'Email', 'SoDienThoai')

@admin.register(models.BaiViet)
class BaiVietAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaNguoiDung', 'ThoiGianTao')
    list_filter = ('MaNguoiDung',)
    search_fields = ('NoiDung',)

@admin.register(models.TepDinhKem)
class TepDinhKemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Tep', 'FileSize', 'MaBaiViet')
    list_filter = ('MaBaiViet',)

@admin.register(models.HinhAnh)
class HinhAnhAdmin(admin.ModelAdmin):
    list_display = ('id', 'Anh', 'ImgSize', 'MaBaiViet')
    list_filter = ('MaBaiViet',)

@admin.register(models.BinhLuan)
class BinhLuanAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaNguoiDung', 'MaBaiViet', 'NgayTao')
    list_filter = ('MaNguoiDung',)
    search_fields = ('NoiDung',)

@admin.register(models.LuotCamXuc)
class LuotCamXucAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaNguoiDung', 'MaBaiViet', 'is_like', 'ThoiGian')
    list_filter = ('is_like',)

# @admin.register(models.CuocTroChuyen)
# class CuocTroChuyenAdmin(admin.ModelAdmin):
#     list_display = ('id', 'Loai', 'TenNhom')
#     search_fields = ('Loai', 'TenNhom')

@admin.register(models.ThanhVienCuocTroChuyen)
class ThanhVienCuocTroChuyenAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaCuocTroChuyen', 'MaNguoiDung', 'NgayGiaNhap')
    list_filter = ('MaCuocTroChuyen',)

@admin.register(models.TinNhanChiTiet)
class TinNhanChiTietAdmin(admin.ModelAdmin):
    list_display = ('id', 'NguoiDung', 'MaCuocTroChuyen', 'NgayTao')
    list_filter = ('NguoiDung',)
    search_fields = ('NoiDung',)

@admin.register(models.BangHoi)
class BangHoiAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaNguoiDung', 'NgayTao')
    list_filter = ('MaNguoiDung',)
    search_fields = ('NoiDung',)

@admin.register(models.BangTL)
class BangTLAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaHoi', 'MaNguoiDung', 'NgayTao')
    list_filter = ('MaHoi',)
    search_fields = ('NoiDung',)

@admin.register(models.BinhChon)
class BinhChonAdmin(admin.ModelAdmin):
    list_display = ('id', 'TenTieuDe', 'MaNguoiDung', 'ThoiGianKetThucBC')
    list_filter = ('MaNguoiDung',)
    search_fields = ('TenTieuDe', 'MoTa')

@admin.register(models.LuaChonBinhChon)
class LuaChonBinhChonAdmin(admin.ModelAdmin):
    list_display = ('id', 'binh_chon', 'noi_dung')
    list_filter = ('binh_chon',)
    search_fields = ('noi_dung',)

@admin.register(models.BinhChonNguoiDung)
class BinhChonNguoiDungAdmin(admin.ModelAdmin):
    list_display = ('id', 'nguoi_dung', 'lua_chon')
    list_filter = ('nguoi_dung',)

@admin.register(models.BinhChonNhom)
class BinhChonNhomAdmin(admin.ModelAdmin):
    list_display = ('id', 'MaPhong', 'MaBinhChon')
    list_filter = ('MaPhong',)
