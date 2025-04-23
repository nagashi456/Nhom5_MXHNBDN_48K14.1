from django.db import models

class PhongBan(models.Model):
    MaPhong = models.AutoField(primary_key=True)
    TenPhong = models.CharField(max_length=255)
    HinhAnhPhong = models.TextField(blank=True, null=True)

class NguoiDung(models.Model):
    MaNguoiDung = models.AutoField(primary_key=True)
    HoTen = models.CharField(max_length=255)
    SoDienThoai = models.CharField(max_length=20)
    VaiTro = models.CharField(max_length=100)
    Email = models.EmailField()
    MaPhong = models.ForeignKey(PhongBan, on_delete=models.CASCADE)

class BaiViet(models.Model):
    MaBaiViet = models.AutoField(primary_key=True)
    NgayTao = models.DateTimeField()
    TepDinhKem = models.TextField(blank=True, null=True)
    HinhAnh = models.TextField(blank=True, null=True)
    NoiDung = models.TextField()
    ThoiGianTao = models.DateTimeField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class TepDinhKem(models.Model):
    MaTepDinhKem = models.AutoField(primary_key=True)
    FileName = models.CharField(max_length=255)
    FilePath = models.TextField()
    FileSize = models.IntegerField()
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

class HinhAnh(models.Model):
    MaHinhAnh = models.AutoField(primary_key=True)
    ImgPath = models.TextField()
    ImgSize = models.IntegerField()
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

class BinhLuan(models.Model):
    MaBinhLuan = models.AutoField(primary_key=True)
    NoiDung = models.TextField()
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class LuotCamXuc(models.Model):
    MaLuotCamXuc = models.AutoField(primary_key=True)
    LoaiCamXuc = models.CharField(max_length=50)
    ThoiGian = models.DateTimeField()
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class CuocTroChuyen(models.Model):
    MaCuocTroChuyen = models.AutoField(primary_key=True)
    Loai = models.CharField(max_length=50)  # cá nhân, nhóm
    TenNhom = models.CharField(max_length=255, blank=True, null=True)
    ThanhVien = models.TextField(blank=True, null=True)
    HinhAnh = models.TextField(blank=True, null=True)

class ThanhVienCuocTroChuyen(models.Model):
    MaThanhVienCuocTroChuyen = models.AutoField(primary_key=True)
    MaCuocTroChuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    NgayGiaNhap = models.DateTimeField()

class TinNhanChiTiet(models.Model):
    MaTinNhan = models.AutoField(primary_key=True)
    NgayTao = models.DateTimeField()
    NoiDung = models.TextField()
    TepDinhKem = models.TextField(blank=True, null=True)
    BieuTuongCamXuc = models.CharField(max_length=50, blank=True, null=True)
    HinhAnh = models.TextField(blank=True, null=True)
    MaCuocTroChuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    NguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class BangHoi(models.Model):
    MaHoi = models.AutoField(primary_key=True)
    NoiDung = models.TextField()
    NgayTao = models.DateTimeField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class BangTL(models.Model):
    MaTL = models.AutoField(primary_key=True)
    NoiDung = models.TextField()
    NgayTao = models.DateTimeField()
    MaHoi = models.ForeignKey(BangHoi, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class BinhChon(models.Model):
    MaBinhChon = models.AutoField(primary_key=True)
    MoTa = models.TextField()
    TenTieuDe = models.CharField(max_length=255)
    ThoiGianKetThucBC = models.DateTimeField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class LuaChonBinhChon(models.Model):
    MaLuaChon = models.AutoField(primary_key=True)
    MaBinhChon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)
    NoiDung = models.TextField()

class NguoiDung_BinhChon(models.Model):
    MaBCNguoiDung = models.AutoField(primary_key=True)
    MaLuaChon = models.ForeignKey(LuaChonBinhChon, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

class BinhChonNhom(models.Model):
    MaNhom = models.IntegerField()
    MaBinhChon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('MaNhom', 'MaBinhChon')
