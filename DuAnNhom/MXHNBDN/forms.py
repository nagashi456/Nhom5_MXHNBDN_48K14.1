from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NguoiDung
from django import forms
from django.forms import inlineformset_factory
from .models import BinhChon, LuaChonBinhChon

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
    extra=3,  # Số lượng form trống ban đầu
    can_delete=True,
    min_num=1,  # Số lượng form tối thiểu
    validate_min=True
)
from django import forms
from .models import BaiViet

class BaiVietForm(forms.ModelForm):
    class Meta:
        model = BaiViet
        fields = ['noi_dung', 'hinh_anh', 'tep_dinh_kem']
        widgets = {
            'noi_dung': forms.Textarea(attrs={
                'placeholder': 'Bạn đang nghĩ gì?',
                'class': 'post-textarea',
                'rows': 10
            }),
            'hinh_anh': forms.FileInput(attrs={
                'class': 'hidden-input',
                'id': 'hinh_anh_input',
                'accept': 'image/*'
            }),
            'tep_dinh_kem': forms.FileInput(attrs={
                'class': 'hidden-input',
                'id': 'tep_dinh_kem_input',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.txt,.zip,.rar'
            }),
        }