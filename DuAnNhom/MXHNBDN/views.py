from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
def DangNhap(request):
    return render(request,"DangNhap.html")


def tao_bai_viet(request):
    # Get the admin user from your custom NguoiDung model
    try:
        # Try to get the first admin user from NguoiDung model
        admin_user = NguoiDung.objects.filter(is_superuser=True).first()
        if not admin_user:
            # If no admin exists, try to get any user
            admin_user = NguoiDung.objects.first()
            if not admin_user:
                # If no users exist, show an error message
                messages.error(request,
                               'Không tìm thấy người dùng nào trong hệ thống. Vui lòng tạo một tài khoản admin trước.')
                return redirect('trang_chu')
    except Exception as e:
        messages.error(request, f'Lỗi khi tìm người dùng: {str(e)}')
        return redirect('trang_chu')

    if request.method == 'POST':
        form = BaiVietForm(request.POST, request.FILES)
        if form.is_valid():
            bai_viet = form.save(commit=False)
            # Use the admin user from NguoiDung model
            bai_viet.nguoi_dung = admin_user
            bai_viet.save()
            messages.success(request, 'Bài viết đã được đăng thành công!')
            return redirect('trang_chu')
    else:
        form = BaiVietForm()

    # Pass the admin username to the template for display
    return render(request, 'TaoBaiViet.html', {
        'form': form,
        'admin_username': admin_user.username
    })
def Binhluan(request):
    return render(request,"TaoBinhLuan/Taobinhluan.html")
# def BinhChon(request):
#     return render(request,"TaoBinhChon/TaoBinhChon.html")
def edit_profile(request):
    return render(request,"Edit_profile/edit_profile.html")
def Nhantin(request):
    return render(request,"NhanTin/NhanTin.html")
def Quenpass(request):
    return render(request,"Quenpass.html")
from django.shortcuts import render, redirect
from .forms import NguoiDungForm, BaiVietForm
from django.contrib import messages
from .forms import LoginForm


def login_view(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang chủ
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            # Chuyển hướng đến trang chủ sau khi đăng nhập thành công
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'DangNhap.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('dang_nhap')

@login_required
def home_view(request):
    return render(request, 'home.html')
def TaoTaiKhoan(request):
    if request.method == 'POST':
        form = NguoiDungForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tạo tài khoản thành công!')
    else:
        form = NguoiDungForm()
    return render(request, 'TaoTaiKhoan/TaoTaiKhoan.html', {'form': form})


def ProfileDetail(request):
    return render(request,"Edit_profile/profile_details.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BinhChon, LuaChonBinhChon, NguoiDung
from .forms import BinhChonForm, LuaChonFormSet

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import BinhChonForm, LuaChonFormSet


def BinhChon(request):
    if request.method == 'POST':
        form = BinhChonForm(request.POST)
        formset = LuaChonFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            binh_chon = form.save(commit=False)

            # Gán người tạo là user có username là "admin"
            User = get_user_model()
            admin_user = get_object_or_404(User, username='admin')
            binh_chon.nguoi_tao = admin_user

            binh_chon.save()

            lua_chon_instances = formset.save(commit=False)
            for lua_chon in lua_chon_instances:
                lua_chon.binh_chon = binh_chon
                lua_chon.save()

            for obj in formset.deleted_objects:
                obj.delete()

            messages.success(request, 'Bình chọn đã được tạo thành công!')
            return redirect('chi_tiet_binh_chon', binh_chon_id=binh_chon.id)
    else:
        form = BinhChonForm()
        formset = LuaChonFormSet()

    return render(request, 'TaoBinhChon/TaoBinhChon.html', {
        'form': form,
        'formset': formset
    })


def TaoBaiViet(request):
    return render(request,"TaoBaiViet/TaoBaiViet.html")
def SuaBaiViet(request):
    return render(request,"SuaBaiViet/SuaBaiViet.html")

def Trangchu(request):
    return render(request,"Trangchu.html")
def Quenpass(request):
    return render(request,"Quenpass.html")