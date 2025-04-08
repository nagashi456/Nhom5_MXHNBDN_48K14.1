from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Người dùng -avatar moi thieu ho ten
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

# Vai trò và quyền hạn - them vao trong nguoi dung khi hien thi html an di nhung van la 1 thuoc tinh
class VaiTro(models.Model):
    ten_vai_tro = models.CharField(max_length=100)

    def __str__(self):
        return self.ten_vai_tro
# xoa phan quyen nay do khong can da co san tren django
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

# Cuoc tro chuyen *
class CuocTroChuyen(models.Model):
    LOAI_TRO_CHUYEN_CHOICES = [
        ('personal', 'Cá nhân'),
        ('group', 'Nhóm'),
    ]
    loai_tro_chuyen = models.CharField(max_length=10, choices=LOAI_TRO_CHUYEN_CHOICES)
    ten_nhom = models.CharField(max_length=255, null=True, blank=True)  # Dành cho nhóm
    thanh_vien = models.ManyToManyField(NguoiDung)

    def save(self, *args, **kwargs):
        # Kiểm tra số thành viên theo loại trò chuyện
        if self.loai_tro_chuyen == 'personal' and self.thanh_vien.count() != 2:
            raise ValueError("Trò chuyện cá nhân phải có đúng 2 người tham gia.")
        if self.loai_tro_chuyen == 'group' and self.thanh_vien.count() < 3:
            raise ValueError("Trò chuyện nhóm phải có ít nhất 3 người tham gia.")
        super().save(*args, **kwargs)

    def __str__(self):
        if self.loai_tro_chuyen == 'personal':
            return f'Trò chuyện cá nhân giữa {", ".join([str(nguoi.username) for nguoi in self.thanh_vien.all()])}'
        return f'Nhóm: {self.ten_nhom or "Cuộc trò chuyện nhóm"}'

# Tin nhắn
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

#Lựa chọn bình chọn *
class LuaChonBinhChon(models.Model):
    binh_chon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)
    noi_dung = models.CharField(max_length=255)
    nguoi_chon=models.ManyToManyField(NguoiDung,through="BinhChonNguoiDung")
    def __str__(self):
        return f'{self.binh_chon.ten_tieu_de} - {self.noi_dung}'
#Bình chọn người dung *
class BinhChonNguoiDung(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    lua_chon = models.ForeignKey(LuaChonBinhChon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nguoi_dung.username} chọn {self.lua_chon.noi_dung}'

# Tạo Nhóm sửa thành nhóm
class Nhom(models.Model):
    ten_nhom = models.CharField(max_length=255)
    hinh_anh_nhom = models.ImageField(upload_to='nhom/', null=True, blank=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    thanhvien= models.ManyToManyField(NguoiDung,through="ThanhVienNhom")
    def __str__(self):
        return self.ten_nhom

class ThanhVienNhom(models.Model):
    nhom = models.ForeignKey(Nhom, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ngay_gia_nhap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nguoi_dung.username} trong {self.nhom.ten_nhom}'


class CauHoi(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)  # Người tạo câu hỏi
    noi_dung = models.TextField()  # Nội dung câu hỏi
    ngay_tao = models.DateTimeField(auto_now_add=True)  # Thời gian tạo câu hỏi

    def __str__(self):
        return f'Câu hỏi của {self.nguoi_dung.username} - {self.noi_dung[:30]}...'
