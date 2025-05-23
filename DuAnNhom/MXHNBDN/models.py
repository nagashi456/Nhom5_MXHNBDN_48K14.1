from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField

baiUser = get_user_model()


class PhongBan(models.Model):
    TenPhong = models.CharField(max_length=255)
    HinhAnhPhong = models.ImageField(upload_to='phong_images/', blank=True, null=True)

    def __str__(self):
        return self.TenPhong


class NguoiDung(models.Model):
    HoTen = models.CharField(max_length=255)
    SoDienThoai = models.CharField(max_length=20)
    Email = models.EmailField()
    Avatar = models.ImageField(upload_to='avatar/',blank=True,null=True);
    AnhBia = models.ImageField(upload_to='anhbia/', blank=True, null=True);
    MaPhong = models.ForeignKey(PhongBan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.HoTen

class BaiViet(models.Model):
    NgayTao = models.DateTimeField()
    NoiDung = models.TextField()
    ThoiGianTao = models.DateTimeField(auto_now_add=True)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bài viết của {self.MaNguoiDung.HoTen} - {self.ThoiGianTao.strftime("%Y-%m-%d %H:%M")}'


class TepDinhKem(models.Model):
    Tep = models.FileField(upload_to='tepdinhkem/')
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

    def __str__(self):
        return self.Tep.name


class HinhAnh(models.Model):
    Anh = models.ImageField(upload_to='hinhanh/')
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)

    def __str__(self):
        return self.Anh.name


class BinhLuan(models.Model):
    NoiDung = models.TextField()
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    NgayTao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.MaNguoiDung.HoTen} bình luận: {self.NoiDung[:30]}'


class LuotCamXuc(models.Model):
    MaBaiViet = models.ForeignKey(BaiViet, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True: like, False: dislike
    ThoiGian = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('MaNguoiDung', 'MaBaiViet')


class CuocTroChuyen(models.Model):
    LoaiRiengTu = models.BooleanField(default=False)
    TenNhom = models.CharField(max_length=255, blank=True, null=True)
    HinhAnh = models.ImageField(upload_to='hinhanhavanhom/')
    ThanhVien = models.ManyToManyField(User,related_name='Cuoc_tro_chuyen')

    def __str__(self):
        return self.TenNhom if self.TenNhom else f'Cuộc trò chuyện {self.id}'


class ThanhVienCuocTroChuyen(models.Model):
    MaCuocTroChuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    NgayGiaNhap = models.DateTimeField()

    def __str__(self):
        return f'{self.MaNguoiDung.HoTen} tham gia {self.MaCuocTroChuyen}'


class TinNhanChiTiet(models.Model):
    NgayTao = models.DateTimeField()
    NoiDung = models.TextField(blank=True, null=True)
    TepDinhKem = models.FileField(upload_to='uploads/attachments/', blank=True, null=True)
    HinhAnh = models.ImageField(upload_to='uploads/images/', blank=True, null=True)
    MaCuocTroChuyen = models.ForeignKey(CuocTroChuyen, on_delete=models.CASCADE)
    NguoiDung = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        username = self.NguoiDung.username

        if self.HinhAnh or getattr(self, 'image_url', None):
            return f'{username}: Ảnh'

        # Trả về file nếu có file đính kèm
        if self.TepDinhKem or getattr(self, 'attachment_url', None):
            return f'{username} : File '
        if self.TepDinhKem or getattr(self, 'attachment_url', None) and self.NoiDung:
            return f'{username} : File + {self.NoiDung[:30]}'
        if self.HinhAnh or getattr(self, 'image_url', None) and self.NoiDung:
            return f'{username}: Ảnh + {self.NoiDung[:30]}'

        # Trả về nội dung text nếu có
        if self.NoiDung:
            return f'{username}: {self.NoiDung[:30]}'

        # Nếu không có gì thì trả về mặc định
        return f'Tin nhắn từ {username}'


class BangHoi(models.Model):
    NoiDung = models.TextField()
    NgayTao = models.DateTimeField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return f'Hỏi bởi {self.MaNguoiDung.HoTen}: {self.NoiDung[:30]}'


class BangTL(models.Model):
    NoiDung = models.TextField()
    NgayTao = models.DateTimeField()
    MaHoi = models.ForeignKey(BangHoi, on_delete=models.CASCADE)
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.MaNguoiDung.HoTen} trả lời: {self.NoiDung[:30]}'




class BinhChon(models.Model):
    MoTa = models.TextField()
    TenTieuDe = models.CharField(max_length=255)
    ThoiGianKetThucBC = models.DateTimeField()
    MaNguoiDung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)

    # Thiết lập quan hệ N-N với PhongBan thông qua bảng trung gian
    PhongBans = models.ManyToManyField(
        PhongBan,
        through='BinhChonNhom',
        related_name='BinhChons'
    )

    def __str__(self):
        return self.TenTieuDe

#Lựa chọn bình chọn *
class LuaChonBinhChon(models.Model):
    binh_chon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)
    noi_dung = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.binh_chon.TenTieuDe} - {self.noi_dung}'
#Bình chọn người dung *
class BinhChonNguoiDung(models.Model):
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    lua_chon = models.ForeignKey(LuaChonBinhChon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nguoi_dung.username} chọn {self.lua_chon.noi_dung}'

class BinhChonNhom(models.Model):
    # FK về PhongBan
    MaPhong = models.ForeignKey(PhongBan, on_delete=models.CASCADE)
    # FK về BinhChon
    MaBinhChon = models.ForeignKey(BinhChon, on_delete=models.CASCADE)

    class Meta:
        # Đảm bảo mỗi cặp (MaPhong, MaBinhChon) chỉ tồn tại một lần
        unique_together = ('MaPhong', 'MaBinhChon')

    def __str__(self):
        return f"{self.MaPhong} ↔ {self.MaBinhChon}"
