from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Người dùng
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

    def __str__(self):
        return self.username

# Vai trò và quyền hạn
class VaiTro(models.Model):
    ten_vai_tro = models.CharField(max_length=100)

    def __str__(self):
        return self.ten_vai_tro

class PhanQuyen(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    vai_tro = models.ForeignKey(VaiTro, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nguoi_dung} - {self.vai_tro}'

# Bài viết
class BaiViet(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    hinh_anh = models.ImageField(upload_to='baiviet/', null=True, blank=True)
    tep_dinh_kem = models.FileField(upload_to='files/', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bài viết của {self.nguoi_dung.username} - {self.ngay_tao.strftime("%d/%m/%Y %H:%M")}'

# Bình luận
class BinhLuan(models.Model):
    bai_viet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nguoi_dung.username} bình luận: {self.noi_dung[:30]}...'

# Nhắn tin
class CuocTroChuyen(models.Model):
    ten_nhom = models.CharField(max_length=255, null=True, blank=True)
    thanh_vien = models.ManyToManyField(NguoiDung)

    def __str__(self):
        if self.ten_nhom:
            return f'Nhóm: {self.ten_nhom}'
        return f'Cuộc trò chuyện #{self.pk}'

class TinNhan(models.Model):
    cuoc_tro_chuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    nguoi_gui = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    tep_dinh_kem = models.FileField(upload_to='messages/', null=True, blank=True)
    hinh_anh = models.ImageField(upload_to='messages/', null=True, blank=True)
    bieu_tuong_cam_xuc = models.CharField(max_length=10, null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nguoi_gui.username}: {self.noi_dung[:30]}...'

# Bình chọn
class BinhChon(models.Model):
    nguoi_tao = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    mo_ta = models.TextField()
    ten_tieu_de = models.CharField(max_length=255)
    thoi_gian_ket_thuc = models.DateTimeField()

    def __str__(self):
        return self.ten_tieu_de

class LuaChonBinhChon(models.Model):
    binh_chon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)
    noi_dung = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.binh_chon.ten_tieu_de} - {self.noi_dung}'

class BinhChonNguoiDung(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    lua_chon = models.ForeignKey(LuaChonBinhChon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nguoi_dung.username} chọn {self.lua_chon.noi_dung}'

# Nhóm
class Nhom(models.Model):
    ten_nhom = models.CharField(max_length=255)
    hinh_anh_nhom = models.ImageField(upload_to='nhom/', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ten_nhom

class ThanhVienNhom(models.Model):
    nhom = models.ForeignKey(Nhom, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_gia_nhap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nguoi_dung.username} trong {self.nhom.ten_nhom}'

# Thông báo
class ThongBao(models.Model):
    nguoi_nhan = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    noi_dung = models.TextField()
    lien_ket = models.URLField(null=True, blank=True)
    da_xem = models.BooleanField(default=False)
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Thông báo đến {self.nguoi_nhan.username}: {self.noi_dung[:40]}...'
