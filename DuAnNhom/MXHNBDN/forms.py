from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NguoiDung
from django import forms
from django.forms import inlineformset_factory
from .models import BinhChon, LuaChonBinhChon
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()  # Lấy model người dùng từ settings.AUTH_USER_MODEL


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
class NguoiDungForm(UserCreationForm):
    class Meta:
        model = NguoiDung
        fields = ['username', 'email', 'so_dien_thoai', 'avatar', 'password1', 'password2', 'vai_tro']
        widgets = {
            'vai_tro': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(NguoiDungForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = 'Điền ở đây'


class BinhChonForm(forms.ModelForm):
    class Meta:
        model = BinhChon
        fields = ['ten_tieu_de', 'mo_ta', 'thoi_gian_ket_thuc']
        widgets = {
            'ten_tieu_de': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tiêu đề bình chọn'
            }),
            'mo_ta': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Nhập mô tả',
                'rows': 5
            }),
            'thoi_gian_ket_thuc': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập thời gian kết thúc bình chọn',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'ten_tieu_de': '',
            'mo_ta': '',
            'thoi_gian_ket_thuc': '',
        }

class LuaChonBinhChonForm(forms.ModelForm):
    class Meta:
        model = LuaChonBinhChon
        fields = ['noi_dung']
        widgets = {
            'noi_dung': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập lựa chọn'
            })
        }
        labels = {
            'noi_dung': '',
        }

# Tạo formset cho các lựa chọn bình chọn
LuaChonFormSet = inlineformset_factory(
    BinhChon,
    LuaChonBinhChon,
    form=LuaChonBinhChonForm,
    extra=3,
    can_delete=True,
    min_num=1,
    validate_min=True
)
