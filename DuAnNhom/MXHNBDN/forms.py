from django.contrib.auth.forms import UserCreationForm
from .models import NguoiDung
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import BinhChon, LuaChonBinhChon
from django.contrib.auth import authenticate, get_user_model
class BaseLuaChonFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('noi_dung') and not form.cleaned_data.get('DELETE', False):
                count += 1

        if count < 2:
            raise forms.ValidationError("Bạn phải nhập ít nhất 2 lựa chọn.")

User = get_user_model()


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
# class NguoiDungForm(UserCreationForm):
#     class Meta:
#         model = NguoiDung
#         fields = ['username', 'email', 'so_dien_thoai', 'avatar', 'password1', 'password2', 'vai_tro']
#         widgets = {
#             'vai_tro': forms.Select(attrs={'class': 'form-input'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(NguoiDungForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-input'
#             field.widget.attrs['placeholder'] = 'Điền ở đây'

from django import forms
from django.forms import inlineformset_factory
from .models import BinhChon, LuaChonBinhChon

class BinhChonForm(forms.ModelForm):
    class Meta:
        model = BinhChon
        fields = ['TenTieuDe', 'ThoiGianKetThucBC', 'MoTa']
        widgets = {
            'TenTieuDe': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập tiêu đề bình chọn',
                'required': True
            }),
            'ThoiGianKetThucBC': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nhập thời gian kết thúc bình chọn',
                'type': 'text',  # sẽ chuyển sang datetime-local khi focus
                'required': True
            }),
            'MoTa': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Nhập mô tả',
                'rows': 5
            }),
        }

# Tạo inline formset để quản lý các lựa chọn của một BinhChon
LuaChonFormSet = inlineformset_factory(
    BinhChon,
    LuaChonBinhChon,
    fields=['noi_dung'],
    extra=0,
    can_delete=True,
    formset=BaseLuaChonFormSet,
    widgets={
        'noi_dung': forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nhập lựa chọn',
            'required': True
        }),
    }
)


# from django import forms
# from .models import BaiViet
#
# class BaiVietForm(forms.ModelForm):
#     class Meta:
#         model = BaiViet
#         fields = ['noi_dung', 'hinh_anh', 'tep_dinh_kem']
#         widgets = {
#             'noi_dung': forms.Textarea(attrs={
#                 'placeholder': 'Bạn đang nghĩ gì?',
#                 'class': 'post-textarea',
#                 'rows': 10
#             }),
#             'hinh_anh': forms.FileInput(attrs={
#                 'class': 'hidden-input',
#                 'id': 'hinh_anh_input',
#                 'accept': 'image/*'
#             }),
#             'tep_dinh_kem': forms.FileInput(attrs={
#                 'class': 'hidden-input',
#                 'id': 'tep_dinh_kem_input',
#                 'accept': '.pdf,.doc,.docx,.xls,.xlsx,.txt,.zip,.rar'
#             }),
#         }
