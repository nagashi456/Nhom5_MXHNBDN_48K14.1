from django.contrib import admin
from .models import (
    PhongBan, NguoiDung, BaiViet, TepDinhKem, HinhAnh,
    BinhLuan, LuotCamXuc, CuocTroChuyen, TinNhanChiTiet,
    BangHoi, BangTL, BinhChon, LuaChonBinhChon,
    BinhChonNguoiDung, BinhChonNhom
)

admin.site.register(PhongBan)
admin.site.register(NguoiDung)
admin.site.register(BaiViet)
admin.site.register(TepDinhKem)
admin.site.register(HinhAnh)
admin.site.register(BinhLuan)
admin.site.register(LuotCamXuc)
admin.site.register(CuocTroChuyen)
admin.site.register(TinNhanChiTiet)
admin.site.register(BangHoi)
admin.site.register(BangTL)
admin.site.register(BinhChon)
admin.site.register(LuaChonBinhChon)
admin.site.register(BinhChonNguoiDung)
admin.site.register(BinhChonNhom)
