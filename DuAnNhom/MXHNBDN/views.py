from django.shortcuts import render
def Binhluan(request):
    return render(request,"TaoBinhLuan/Taobinhluan.html")
# def BinhChon(request):
#     return render(request,"TaoBinhChon/TaoBinhChon.html")
def edit_profile(request):
    return render(request,"Edit_profile/edit_profile.html")
def Nhantin(request):
    return render(request,"NhanTin/NhanTin.html")
from django.shortcuts import render, redirect
from .forms import NguoiDungForm
from django.contrib import messages

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
from .models import BinhChon, LuaChonBinhChon
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
