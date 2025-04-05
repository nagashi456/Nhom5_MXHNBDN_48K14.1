
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class NguoiDung(AbstractUser):
    so_dien_thoai = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='nguoidung_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='nguoidung_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Tài khoản (đã gộp vào AbstractUser)

# Vai trò và quyền hạn
class VaiTro(models.Model):
    ten_vai_tro = models.CharField(max_length=100)

class PhanQuyen(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    vai_tro = models.ForeignKey(VaiTro, on_delete=models.CASCADE)

# Bài viết
class BaiViet(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    hinh_anh = models.ImageField(upload_to='baiviet/', null=True, blank=True)
    tep_dinh_kem = models.FileField(upload_to='files/', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

# Bình luận
class BinhLuan(models.Model):
    bai_viet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(auto_now_add=True)

# Nhắn tin
class CuocTroChuyen(models.Model):
    ten_nhom = models.CharField(max_length=255, null=True, blank=True)
    thanh_vien = models.ManyToManyField(NguoiDung)

class TinNhan(models.Model):
    cuoc_tro_chuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    tep_dinh_kem = models.FileField(upload_to='messages/', null=True, blank=True)
    hinh_anh = models.ImageField(upload_to='messages/', null=True, blank=True)
    bieu_tuong_cam_xuc = models.CharField(max_length=10, null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

# Bình chọn
class BinhChon(models.Model):
    nguoi_tao = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    mo_ta = models.TextField()
    ten_tieu_de = models.CharField(max_length=255)
    thoi_gian_ket_thuc = models.DateTimeField()

class LuaChonBinhChon(models.Model):
    binh_chon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)
    noi_dung = models.CharField(max_length=255)

class BinhChonNguoiDung(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    lua_chon = models.ForeignKey(LuaChonBinhChon, on_delete=models.CASCADE)

# Nhóm
class Nhom(models.Model):
    ten_nhom = models.CharField(max_length=255)
    hinh_anh_nhom = models.ImageField(upload_to='nhom/', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

class ThanhVienNhom(models.Model):
    nhom = models.ForeignKey(Nhom, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_gia_nhap = models.DateTimeField(auto_now_add=True)

# Thông báo
class ThongBao(models.Model):
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    lien_ket = models.URLField(null=True, blank=True)
    da_xem = models.BooleanField(default=False)
    ngay_tao = models.DateTimeField(auto_now_add=True)

# Create your models here.