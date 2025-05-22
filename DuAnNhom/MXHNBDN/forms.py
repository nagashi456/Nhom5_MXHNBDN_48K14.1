from django.utils import timezone
from .models import PhongBan
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import BinhChon, LuaChonBinhChon
from django.contrib.auth import authenticate, get_user_model
from django import forms
from .models import BaiViet, HinhAnh, TepDinhKem
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from .models import NguoiDung

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Mật khẩu không khớp")
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class NguoiDungForm(forms.ModelForm):
    class Meta:
        model = NguoiDung
        fields = ['HoTen', 'SoDienThoai', 'Email', 'MaPhong', 'Avatar', 'AnhBia']

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='Tên đăng nhập hoặc Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên đăng nhập hoặc email'})
    )
    password = forms.CharField(
        label='Mật khẩu',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            # Thử xác thực với tên đăng nhập
            user = authenticate(username=username_or_email, password=password)

            # Nếu không thành công, thử với email
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if not user:
                raise forms.ValidationError('Tên đăng nhập hoặc mật khẩu không đúng')

            cleaned_data['user'] = user

        return cleaned_data
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import NguoiDung

class UserProfileForm(forms.ModelForm):
    """Form cho thông tin người dùng cơ bản"""
    class Meta:
        model = NguoiDung
        fields = ['HoTen', 'Email', 'SoDienThoai', 'Avatar', 'AnhBia']
        widgets = {
            'HoTen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'SoDienThoai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'Avatar': forms.FileInput(attrs={'class': 'form-control-file', 'style': 'display: none;', 'id': 'avatar-upload'}),
            'AnhBia': forms.FileInput(attrs={'class': 'form-control-file', 'style': 'display: none;', 'id': 'cover-upload'}),
        }
        labels = {
            'HoTen': 'Họ tên',
            'Email': 'Email',
            'SoDienThoai': 'Số điện thoại',
            'Avatar': 'Ảnh đại diện',
            'AnhBia': 'Ảnh bìa',
        }

class UsernameChangeForm(forms.ModelForm):
    """Form cho việc thay đổi tên đăng nhập"""
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập mới'})
        }
        labels = {
            'username': 'Tên đăng nhập',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Form tùy chỉnh cho việc thay đổi mật khẩu"""
    old_password = forms.CharField(
        label="Mật khẩu cũ",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu cũ'}),
    )
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu mới'}),
    )
    new_password2 = forms.CharField(
        label="Xác nhận mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu mới'}),
    )





class UserProfileForm(forms.ModelForm):
    """Form cho thông tin người dùng cơ bản"""
    class Meta:
        model = NguoiDung
        fields = ['HoTen', 'Email', 'SoDienThoai', 'Avatar', 'AnhBia']
        widgets = {
            'HoTen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'SoDienThoai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'Avatar': forms.FileInput(attrs={'class': 'form-control-file', 'style': 'display: none;', 'id': 'avatar-upload'}),
            'AnhBia': forms.FileInput(attrs={'class': 'form-control-file', 'style': 'display: none;', 'id': 'cover-upload'}),
        }
        labels = {
            'HoTen': 'Họ tên',
            'Email': 'Email',
            'SoDienThoai': 'Số điện thoại',
            'Avatar': 'Ảnh đại diện',
            'AnhBia': 'Ảnh bìa',
        }

class UsernameChangeForm(forms.ModelForm):
    """Form cho việc thay đổi tên đăng nhập"""
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập mới'})
        }
        labels = {
            'username': 'Tên đăng nhập',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Mật khẩu cũ",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu cũ'}),
    )
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nhập mật khẩu mới'}),
    )
    new_password2 = forms.CharField(
        label="Xác nhận mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu mới'}),
    )



class LuaChonBinhChonForm(forms.ModelForm):
    class Meta:
        model = LuaChonBinhChon
        fields = ['noi_dung']
        widgets = {
            'noi_dung': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập lựa chọn'
            })
        }


class BinhChonForm(forms.ModelForm):
    phong_ban = forms.ModelMultipleChoiceField(
        queryset=PhongBan.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'phong-ban-checkbox'}),
        required=True,
        label="Phòng ban"
    )

    class Meta:
        model = BinhChon
        fields = ['TenTieuDe', 'ThoiGianKetThucBC', 'MoTa']
        widgets = {
            'TenTieuDe': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề bình chọn'
            }),
            'ThoiGianKetThucBC': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Nhập thời gian kết thúc bình chọn'
            }),
            'MoTa': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập mô tả (tùy chọn)',
                'rows': 4
            }),
        }
        labels = {
            'TenTieuDe': 'Tiêu đề',
            'ThoiGianKetThucBC': 'Thời gian kết thúc',
            'MoTa': 'Mô tả',
        }

    def clean_ThoiGianKetThucBC(self):
        end_date = self.cleaned_data.get('ThoiGianKetThucBC')
        if end_date and end_date < timezone.now():
            raise ValidationError("Thời gian kết thúc không được nhỏ hơn thời gian hiện tại.")
        return end_date


# Tạo formset cho các lựa chọn bình chọn
LuaChonBinhChonFormSet = inlineformset_factory(
    BinhChon,
    LuaChonBinhChon,
    form=LuaChonBinhChonForm,
    extra=4,  # Số lượng form trống ban đầu
    min_num=2,  # Số lượng form tối thiểu
    validate_min=True,  # Bắt buộc phải có ít nhất min_num form
    can_delete=True
)
from django import forms
from .models import BaiViet
from django.utils import timezone


class BaiVietForm(forms.ModelForm):
    noi_dung = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control post-textarea',
                'placeholder': 'Bạn đang nghĩ gì?',
                'rows': 5
            }
        )
    )

    class Meta:
        model = BaiViet
        fields = ['noi_dung']

    def save(self, commit=True, nguoi_dung=None):
        bai_viet = super().save(commit=False)
        bai_viet.MaNguoiDung = nguoi_dung
        bai_viet.NgayTao = timezone.now()

        if commit:
            bai_viet.save()
        return bai_viet