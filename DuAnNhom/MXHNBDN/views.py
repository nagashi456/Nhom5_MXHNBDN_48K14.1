from django.shortcuts import render, get_object_or_404
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
# from .forms import NguoiDungForm, BaiVietForm
from django.contrib import messages
from .forms import LoginForm


def login_view(request):
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang chủ
    if request.user.is_authenticated:
        return redirect('trang_chu')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            # Chuyển hướng đến trang chủ sau khi đăng nhập thành công
            return redirect('trang_chu')
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
from .models import NguoiDung, BinhChon
from .forms import BinhChonForm, LuaChonFormSet


@login_required
def tao_binh_chon(request):
    try:
        nguoi_dung = NguoiDung.objects.get(Email=request.user.email)
    except NguoiDung.DoesNotExist:
        messages.error(request, "Tài khoản của bạn chưa được liên kết với bảng NguoiDung.")
        return redirect('profile_detail')

    if request.method == 'POST':
        form = BinhChonForm(request.POST)
        formset = LuaChonFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Lưu bình chọn
            binh_chon = form.save(commit=False)
            binh_chon.MaNguoiDung = nguoi_dung
            binh_chon.save()

            # Gán formset instance và lưu các lựa chọn
            formset.instance = binh_chon
            formset.save()

            return redirect('chi-tiet-binh-chon', pk=binh_chon.MaBinhChon)
    else:
        form = BinhChonForm()
        formset = LuaChonFormSet()

    return render(request, 'TaoBinhChon/TaoBinhChon.html', {
        'form': form,
        'formset': formset,
        'vai_tro': nguoi_dung.VaiTro,
    })
def chi_tiet_binh_chon(request, pk):
    binh_chon = get_object_or_404(BinhChon, pk=pk)
    return render(request, 'binh_chon/chi_tiet.html', {'binh_chon': binh_chon})
from django.forms import BaseInlineFormSet





def TaoBaiViet(request):
    return render(request,"TaoBaiViet/TaoBaiViet.html")
def SuaBaiViet(request):
    return render(request,"SuaBaiViet/SuaBaiViet.html")
@login_required
def Trangchu(request):
    return render(request,"Trangchu.html")
def Quenpass(request):
    return render(request,"Quenpass.html")