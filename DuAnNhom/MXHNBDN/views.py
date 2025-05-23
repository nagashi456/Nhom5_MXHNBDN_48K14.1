from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, UsernameChangeForm, CustomPasswordChangeForm, LuaChonBinhChonFormSet
from .models import BaiViet, BinhChonNhom
from .forms import BinhChonForm
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, NguoiDungForm
from .models import (
    CuocTroChuyen, TinNhanChiTiet,
    ThanhVienCuocTroChuyen
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



def DangNhap(request):
    return render(request,"DangNhap.html")

def Binhluan(request):
    return render(request,"TaoBinhLuan/Taobinhluan.html")
# def BinhChon(request):
#     return render(request,"TaoBinhChon/TaoBinhChon.html")
def Nhantin(request):
    return render(request,"NhanTin/NhanTin.html")
def Quenpass(request):
    return render(request,"Quenpass.html")
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





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BaiVietForm
from .models import NguoiDung, HinhAnh, TepDinhKem, BaiViet
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BaiVietForm
from .models import NguoiDung, HinhAnh, TepDinhKem, BaiViet
from django.utils import timezone


@login_required
def tao_bai_viet(request):
    try:
        nguoi_dung = NguoiDung.objects.get(user=request.user)

        if request.method == 'POST':
            form = BaiVietForm(request.POST)

            if form.is_valid():
                # Tạo bài viết mới
                bai_viet = BaiViet(
                    NgayTao=timezone.now(),
                    NoiDung=form.cleaned_data['noi_dung'],
                    MaNguoiDung=nguoi_dung
                )
                bai_viet.save()

                # Xử lý hình ảnh
                if 'hinh_anh[]' in request.FILES:
                    for anh in request.FILES.getlist('hinh_anh[]'):

                        # Lưu hình ảnh
                        hinh_anh = HinhAnh(
                            Anh=anh,
                            MaBaiViet=bai_viet
                        )
                        hinh_anh.save()

                # Xử lý tệp đính kèm
                if 'tep_dinh_kem[]' in request.FILES:
                    for tep in request.FILES.getlist('tep_dinh_kem[]'):

                        # Lưu tệp
                        tep_dinh_kem = TepDinhKem(
                            Tep=tep,
                            MaBaiViet=bai_viet
                        )
                        tep_dinh_kem.save()

                messages.success(request, 'Bài viết đã được tạo thành công!')
                return redirect('trang_chu')
            else:
                # In ra lỗi để debug
                print(form.errors)
                messages.error(request, 'Có lỗi xảy ra khi tạo bài viết.')
        else:
            form = BaiVietForm()

        context = {
            'form': form,
            'nguoidung': nguoi_dung,
        }

        return render(request, 'BaiViet/TaoBaiViet.html', context)
    except Exception as e:
        # In ra lỗi để debug
        print(f"Lỗi: {e}")
        messages.error(request, f"Đã xảy ra lỗi: {e}")
        return redirect('trang_chu')





@login_required
def TaoTaiKhoan(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = NguoiDungForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Lưu user mới
            user = user_form.save()

            # Lưu profile (NguoiDung) liên kết với user đó
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Thêm message thành công, rồi redirect về trang chủ
            messages.success(request, "Tạo tài khoản nhân viên thành công!")
            return redirect('trang_chu')  # 'trang_chu' là name của URL trang chủ

        # Nếu có lỗi, rơi xuống phía dưới để render lại cùng lỗi
    else:
        user_form = UserRegistrationForm()
        profile_form = NguoiDungForm()

    phong_ban_list = PhongBan.objects.all()
    return render(request, 'TaoTaiKhoan/TaoTaiKhoan.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'phong_ban_list': phong_ban_list,
    })


from django.contrib.auth import update_session_auth_hash

@login_required
def edit_profile(request):
    user = request.user
    try:
        nguoi_dung = NguoiDung.objects.get(user=user)
    except NguoiDung.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin người dùng")
        return redirect('trang_chu')

    post_count = BaiViet.objects.filter(MaNguoiDung=nguoi_dung).count()

    profile_form = UserProfileForm(instance=nguoi_dung)
    username_form = UsernameChangeForm(instance=user)
    password_form = CustomPasswordChangeForm(user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=nguoi_dung)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Cập nhật thông tin cá nhân thành công!")
                return redirect('edit_profile')

        elif action == 'username':
            username_form = UsernameChangeForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, "Cập nhật tên đăng nhập thành công!")
                return redirect('edit_profile')

        elif action == 'password':
            password_form = CustomPasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Cập nhật mật khẩu thành công!")
                return redirect('edit_profile')

    context = {
        'profile_form': profile_form,
        'username_form': username_form,
        'password_form': password_form,
        'nguoi_dung': nguoi_dung,
        'post_count': post_count,
        'hide_sidebar': False,
        'show_search': False,
    }
    return render(request, 'Edit_Profile/edit_profile.html', context)

from .models import NguoiDung


@login_required
def tao_binh_chon(request):
    nguoi_dung = NguoiDung.objects.get(user=request.user)

    if request.method == 'POST':
        form = BinhChonForm(request.POST)
        formset = LuaChonBinhChonFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Lưu bình chọn
            binh_chon = form.save(commit=False)
            binh_chon.MaNguoiDung = nguoi_dung
            binh_chon.save()

            # Lưu các lựa chọn
            formset.instance = binh_chon
            formset.save()

            # Lưu các phòng ban được chọn
            phong_ban_ids = request.POST.getlist('phong_ban')
            for pb_id in phong_ban_ids:
                BinhChonNhom.objects.create(
                    MaPhong_id=pb_id,
                    MaBinhChon=binh_chon
                )

            messages.success(request, 'Tạo bình chọn thành công!')
            return redirect('danh_sach_binh_chon')  # Chuyển hướng đến trang danh sách bình chọn
    else:
        form = BinhChonForm()
        formset = LuaChonBinhChonFormSet()

    context = {
        'form': form,
        'formset': formset,
        'phong_bans': PhongBan.objects.all(),
        'nguoidung': nguoi_dung,  # Thêm thông tin người dùng cho template
    }
    return render(request, 'BinhChon/TaoBinhChon.html', context)


@login_required
def danh_sach_binh_chon(request):
    nguoi_dung = NguoiDung.objects.get(user=request.user)
    binh_chons = BinhChon.objects.all().order_by('-ThoiGianKetThucBC')

    context = {
        'binh_chons': binh_chons,
        'nguoidung': nguoi_dung,  # Thêm thông tin người dùng cho template
    }
    return render(request, 'BinhChon/danh_sach_binh_chon.html', context)

def current_profile(request):
    """
    Trả về {'nguoidung': <NguoiDung instance> hoặc None}
    nếu user đã login và có bản NguoiDung đầu tiên.
    """
    if request.user.is_authenticated:
        # với ForeignKey: lấy bản đầu tiên
        profile = request.user.nguoidung_set.first()
        return {'nguoidung': profile}
    return {'nguoidung': None}


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q
from .models import (
    PhongBan, NguoiDung, BaiViet, TepDinhKem, HinhAnh, BinhLuan,
    LuotCamXuc, BinhChon, LuaChonBinhChon, BinhChonNguoiDung
)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import NguoiDung, BaiViet

@login_required

def profile_view(request):
    profile_user = get_object_or_404(NguoiDung, user=request.user)
    posts = BaiViet.objects.filter(MaNguoiDung=profile_user).order_by('-ThoiGianTao')
    return render(request, 'edit_profile/profile_details.html', {
        'profile_user': profile_user,
        'posts': posts
    })
@login_required
def ProfileDetail(request):
    # Lấy profile
    try:
        nguoi_dung = NguoiDung.objects.get(user=request.user)
    except NguoiDung.DoesNotExist:
        return HttpResponse("Không tìm thấy hồ sơ người dùng", status=404)

    # BÀI VIẾT
    bai_viet_list = BaiViet.objects.filter(MaNguoiDung=nguoi_dung).order_by('-ThoiGianTao')
    # map trạng thái like/dislike của user
    cx_map = {
        cx.MaBaiViet.id: cx.is_like
        for cx in LuotCamXuc.objects.filter(MaNguoiDung=nguoi_dung)
    }
    for bv in bai_viet_list:
        bv.so_thich = LuotCamXuc.objects.filter(MaBaiViet=bv, is_like=True).count()
        bv.so_khong_thich = LuotCamXuc.objects.filter(MaBaiViet=bv, is_like=False).count()
        bv.da_thich = cx_map.get(bv.id)  # True / False / None
        bv.binh_luan_list = BinhLuan.objects.filter(MaBaiViet=bv).order_by('-NgayTao')
        bv.so_binh_luan = bv.binh_luan_list.count()
        bv.anh_list = HinhAnh.objects.filter(MaBaiViet=bv)
        bv.file_list = TepDinhKem.objects.filter(MaBaiViet=bv)

    # BÌNH CHỌN
    binh_chon_list = BinhChon.objects.filter(MaNguoiDung=nguoi_dung).order_by('-ThoiGianKetThucBC')
    # map lựa chọn user đã bình chọn
    bc_map = {
        bcnd.lua_chon.binh_chon.id: bcnd.lua_chon.id
        for bcnd in BinhChonNguoiDung.objects.filter(nguoi_dung=nguoi_dung)
    }
    for bc in binh_chon_list:
        # list các lựa chọn và số vote
        bc.lua_chon_list = LuaChonBinhChon.objects.filter(binh_chon=bc)
        bc.tong_vote = 0
        for lc in bc.lua_chon_list:
            lc.so_vote = BinhChonNguoiDung.objects.filter(lua_chon=lc).count()
            bc.tong_vote += lc.so_vote
        # thời gian còn lại
        if bc.ThoiGianKetThucBC > timezone.now():
            delta = bc.ThoiGianKetThucBC - timezone.now()
            bc.thoi_gian_con_lai = f"{delta.days}d {delta.seconds // 3600}h"
        else:
            bc.thoi_gian_con_lai = "Đã kết thúc"
        # user đã chọn
        bc.da_chon = bc_map.get(bc.id)

    # Chọn tab
    tab = request.GET.get('tab', 'baiviet')

    return render(request, 'Edit_profile/profile_details.html', {
        'nguoi_dung': nguoi_dung,
        'bai_viet_list': bai_viet_list,
        'binh_chon_list': binh_chon_list,
        'tab': tab,
    })

@login_required
def trang_chu(request):
    # Lấy người dùng hiện tại
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)
    phong_ban = nguoi_dung.MaPhong

    # Lấy danh sách bài viết
    bai_viet_list = BaiViet.objects.all().order_by('-ThoiGianTao')

    # Lấy danh sách bình chọn cho phòng ban của người dùng
    binh_chon_list = BinhChon.objects.filter(
        PhongBans=phong_ban
    ).order_by('-ThoiGianKetThucBC')

    # Lấy thông tin về lượt thích và bình chọn của người dùng
    luot_cam_xuc_nguoi_dung = {
        lcx.MaBaiViet.id: lcx.is_like
        for lcx in LuotCamXuc.objects.filter(MaNguoiDung=nguoi_dung)
    }

    binh_chon_nguoi_dung = {
        bcnd.lua_chon.binh_chon.id: bcnd.lua_chon.id
        for bcnd in BinhChonNguoiDung.objects.filter(nguoi_dung=nguoi_dung)
    }

    # Đếm số lượt thích và không thích cho mỗi bài viết
    for bai_viet in bai_viet_list:
        bai_viet.so_luot_thich = LuotCamXuc.objects.filter(
            MaBaiViet=bai_viet, is_like=True
        ).count()
        bai_viet.so_luot_khong_thich = LuotCamXuc.objects.filter(
            MaBaiViet=bai_viet, is_like=False
        ).count()
        bai_viet.hinh_anh_list = HinhAnh.objects.filter(MaBaiViet=bai_viet)
        bai_viet.tep_dinh_kem_list = TepDinhKem.objects.filter(MaBaiViet=bai_viet)
        bai_viet.binh_luan_list = BinhLuan.objects.filter(MaBaiViet=bai_viet).order_by('-NgayTao')

        # Kiểm tra người dùng đã thích hay không thích bài viết
        if bai_viet.id in luot_cam_xuc_nguoi_dung:
            bai_viet.da_thich = luot_cam_xuc_nguoi_dung[bai_viet.id]
        else:
            bai_viet.da_thich = None

    # Đếm số lượt bình chọn cho mỗi lựa chọn
    for binh_chon in binh_chon_list:
        binh_chon.lua_chon_list = LuaChonBinhChon.objects.filter(binh_chon=binh_chon)

        # Tính tổng số bình chọn
        tong_so_binh_chon = 0
        for lua_chon in binh_chon.lua_chon_list:
            lua_chon.so_luot_chon = BinhChonNguoiDung.objects.filter(lua_chon=lua_chon).count()
            tong_so_binh_chon += lua_chon.so_luot_chon

        binh_chon.tong_so_binh_chon = tong_so_binh_chon

        # Tính thời gian còn lại
        if binh_chon.ThoiGianKetThucBC > timezone.now():
            thoi_gian_con_lai = binh_chon.ThoiGianKetThucBC - timezone.now()
            days = thoi_gian_con_lai.days
            hours, remainder = divmod(thoi_gian_con_lai.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            if days > 0:
                binh_chon.thoi_gian_con_lai = f"Còn {days} ngày {hours} giờ"
            elif hours > 0:
                binh_chon.thoi_gian_con_lai = f"Còn {hours} giờ {minutes} phút"
            else:
                binh_chon.thoi_gian_con_lai = f"Còn {minutes} phút"
        else:
            binh_chon.thoi_gian_con_lai = "Đã kết thúc"

        # Kiểm tra người dùng đã bình chọn hay chưa
        if binh_chon.id in binh_chon_nguoi_dung:
            binh_chon.lua_chon_da_chon = binh_chon_nguoi_dung[binh_chon.id]
        else:
            binh_chon.lua_chon_da_chon = None

    context = {
        'nguoidung': nguoi_dung,
        'bai_viet_list': bai_viet_list,
        'binh_chon_list': binh_chon_list,
    }

    return render(request, 'TrangChu.html', context)


@login_required
def them_binh_luan(request, bai_viet_id):
    if request.method == 'POST':
        noi_dung = request.POST.get('NoiDung')
        if noi_dung:
            bai_viet = get_object_or_404(BaiViet, id=bai_viet_id)
            nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

            BinhLuan.objects.create(
                NoiDung=noi_dung,
                MaBaiViet=bai_viet,
                MaNguoiDung=nguoi_dung,
                NgayTao=timezone.now()
            )

    return redirect('trang_chu')

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

@login_required
def xu_ly_cam_xuc(request):
    if request.method == 'POST':
        bai_viet_id = request.POST.get('bai_viet_id')
        loai_cam_xuc = request.POST.get('loai_cam_xuc') == 'true'

        bai_viet = get_object_or_404(BaiViet, id=bai_viet_id)
        nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

        try:
            luot_cam_xuc = LuotCamXuc.objects.get(
                MaBaiViet=bai_viet,
                MaNguoiDung=nguoi_dung
            )

            if luot_cam_xuc.is_like == loai_cam_xuc:
                # Đã bày tỏ cùng loại cảm xúc, không làm gì thêm
                action = 'unchanged'
            else:
                # Cập nhật sang loại cảm xúc mới
                luot_cam_xuc.is_like = loai_cam_xuc
                luot_cam_xuc.ThoiGian = timezone.now()
                luot_cam_xuc.save()
                action = 'changed'

        except LuotCamXuc.DoesNotExist:
            # Chưa có cảm xúc trước đó → tạo mới
            LuotCamXuc.objects.create(
                MaBaiViet=bai_viet,
                MaNguoiDung=nguoi_dung,
                is_like=loai_cam_xuc,
                ThoiGian=timezone.now()
            )
            action = 'added'

        # Đếm số lượt thích và không thích
        so_luot_thich = LuotCamXuc.objects.filter(
            MaBaiViet=bai_viet, is_like=True
        ).count()
        so_luot_khong_thich = LuotCamXuc.objects.filter(
            MaBaiViet=bai_viet, is_like=False
        ).count()

        return JsonResponse({
            'success': True,
            'action': action,
            'so_luot_thich': so_luot_thich,
            'so_luot_khong_thich': so_luot_khong_thich
        })

    return JsonResponse({'success': False})



@login_required
def xu_ly_binh_chon(request):
    if request.method == 'POST':
        lua_chon_id = request.POST.get('lua_chon_id')

        lua_chon = get_object_or_404(LuaChonBinhChon, id=lua_chon_id)
        nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

        # Kiểm tra xem người dùng đã bình chọn cho bình chọn này chưa
        binh_chon_cu = BinhChonNguoiDung.objects.filter(
            nguoi_dung=nguoi_dung,
            lua_chon__binh_chon=lua_chon.binh_chon
        ).first()

        if binh_chon_cu:
            # Nếu đã chọn cùng lựa chọn, xóa bình chọn
            if binh_chon_cu.lua_chon.id == lua_chon.id:
                binh_chon_cu.delete()
                action = 'removed'
            else:
                # Nếu đã chọn lựa chọn khác, cập nhật
                binh_chon_cu.lua_chon = lua_chon
                binh_chon_cu.save()
                action = 'changed'
        else:
            # Nếu chưa bình chọn, tạo mới
            BinhChonNguoiDung.objects.create(
                nguoi_dung=nguoi_dung,
                lua_chon=lua_chon
            )
            action = 'added'

        # Đếm số lượt cho mỗi lựa chọn trong bình chọn
        lua_chon_list = LuaChonBinhChon.objects.filter(binh_chon=lua_chon.binh_chon)
        ket_qua = {}

        for lc in lua_chon_list:
            ket_qua[lc.id] = BinhChonNguoiDung.objects.filter(lua_chon=lc).count()

        return JsonResponse({
            'success': True,
            'action': action,
            'ket_qua': ket_qua
        })

    return JsonResponse({'success': False})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from .models import (
    PhongBan, NguoiDung, BaiViet, TepDinhKem, HinhAnh, BinhLuan,
    LuotCamXuc, BinhChon, LuaChonBinhChon, BinhChonNguoiDung
)


# Các view hiện tại giữ nguyên

@login_required
def sua_bai_viet(request, bai_viet_id):
    bai_viet = get_object_or_404(BaiViet, id=bai_viet_id)
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

    # Kiểm tra quyền sửa bài viết
    if bai_viet.MaNguoiDung.user.id != request.user.id:
        return HttpResponseForbidden("Bạn không có quyền sửa bài viết này.")

    hinh_anh_list = HinhAnh.objects.filter(MaBaiViet=bai_viet)
    tep_dinh_kem_list = TepDinhKem.objects.filter(MaBaiViet=bai_viet)

    if request.method == 'POST':
        # Cập nhật nội dung bài viết
        noi_dung = request.POST.get('NoiDung')
        bai_viet.NoiDung = noi_dung
        bai_viet.save()

        # Xử lý xóa hình ảnh
        hinh_anh_xoa = request.POST.getlist('hinh_anh_xoa')
        for hinh_anh_id in hinh_anh_xoa:
            try:
                hinh_anh = HinhAnh.objects.get(id=hinh_anh_id, MaBaiViet=bai_viet)
                hinh_anh.delete()
            except HinhAnh.DoesNotExist:
                pass

        # Xử lý xóa tệp đính kèm
        tep_xoa = request.POST.getlist('tep_xoa')
        for tep_id in tep_xoa:
            try:
                tep = TepDinhKem.objects.get(id=tep_id, MaBaiViet=bai_viet)
                tep.delete()
            except TepDinhKem.DoesNotExist:
                pass

        # Xử lý thêm hình ảnh mới
        hinh_anh_moi = request.FILES.getlist('hinh_anh_moi')
        for hinh_anh in hinh_anh_moi:
            if hinh_anh:
                HinhAnh.objects.create(
                    Anh=hinh_anh,
                    MaBaiViet=bai_viet
                )

        # Xử lý thêm tệp đính kèm mới
        tep_dinh_kem_moi = request.FILES.getlist('tep_dinh_kem_moi')
        for tep in tep_dinh_kem_moi:
            if tep:
                TepDinhKem.objects.create(
                    Tep=tep,
                    MaBaiViet=bai_viet
                )

        messages.success(request, "Bài viết đã được cập nhật thành công.")
        return redirect('trang_chu')

    context = {
        'bai_viet': bai_viet,
        'hinh_anh_list': hinh_anh_list,
        'tep_dinh_kem_list': tep_dinh_kem_list,
        'nguoidung': nguoi_dung,
    }

    return render(request, 'BaiViet/SuaBaiViet.html', context)


@login_required
def xoa_bai_viet(request, bai_viet_id):
    bai_viet = get_object_or_404(BaiViet, id=bai_viet_id)

    # Kiểm tra quyền xóa bài viết
    if bai_viet.MaNguoiDung.user.id != request.user.id:
        return HttpResponseForbidden("Bạn không có quyền xóa bài viết này.")

    # Xóa bài viết
    bai_viet.delete()

    messages.success(request, "Bài viết đã được xóa thành công.")
    return redirect('trang_chu')


@login_required
def sua_binh_chon(request, binh_chon_id):
    binh_chon = get_object_or_404(BinhChon, id=binh_chon_id)
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

    # Kiểm tra quyền sửa bình chọn
    if binh_chon.MaNguoiDung.user.id != request.user.id:
        return HttpResponseForbidden("Bạn không có quyền sửa bình chọn này.")

    lua_chon_list = LuaChonBinhChon.objects.filter(binh_chon=binh_chon)
    phong_ban_list = PhongBan.objects.all()
    phong_ban_da_chon = binh_chon.PhongBans.all()

    if request.method == 'POST':
        # Cập nhật thông tin bình chọn
        tieu_de = request.POST.get('TenTieuDe')
        mo_ta = request.POST.get('MoTa')
        thoi_gian_ket_thuc = request.POST.get('ThoiGianKetThucBC')

        binh_chon.TenTieuDe = tieu_de
        binh_chon.MoTa = mo_ta
        if thoi_gian_ket_thuc:
            binh_chon.ThoiGianKetThucBC = thoi_gian_ket_thuc
        binh_chon.save()

        # Cập nhật phòng ban
        binh_chon.PhongBans.clear()
        phong_ban_ids = request.POST.getlist('phong_ban')
        for pb_id in phong_ban_ids:
            phong_ban = PhongBan.objects.get(id=pb_id)
            binh_chon.PhongBans.add(phong_ban)

        # Xử lý xóa lựa chọn
        lua_chon_xoa = request.POST.getlist('lua_chon_xoa')
        for lua_chon_id in lua_chon_xoa:
            try:
                lua_chon = LuaChonBinhChon.objects.get(id=lua_chon_id, binh_chon=binh_chon)
                lua_chon.delete()
            except LuaChonBinhChon.DoesNotExist:
                pass

        # Cập nhật lựa chọn hiện tại
        for lua_chon in lua_chon_list:
            noi_dung_moi = request.POST.get(f'lua_chon_{lua_chon.id}')
            if noi_dung_moi:
                lua_chon.noi_dung = noi_dung_moi
                lua_chon.save()

        # Thêm lựa chọn mới
        lua_chon_moi = request.POST.getlist('lua_chon_moi')
        for noi_dung in lua_chon_moi:
            if noi_dung:
                LuaChonBinhChon.objects.create(
                    binh_chon=binh_chon,
                    noi_dung=noi_dung
                )

        messages.success(request, "Bình chọn đã được cập nhật thành công.")
        return redirect('trang_chu')

    context = {
        'binh_chon': binh_chon,
        'lua_chon_list': lua_chon_list,
        'phong_ban_list': phong_ban_list,
        'phong_ban_da_chon': phong_ban_da_chon,
        'nguoidung': nguoi_dung,
    }

    return render(request,  'BinhChon/sua_binh_chon.html', context)


@login_required
def xoa_binh_chon(request, binh_chon_id):
    binh_chon = get_object_or_404(BinhChon, id=binh_chon_id)

    # Kiểm tra quyền xóa bình chọn
    if binh_chon.MaNguoiDung.user.id != request.user.id:
        return HttpResponseForbidden("Bạn không có quyền xóa bình chọn này.")

    # Xóa bình chọn
    binh_chon.delete()

    messages.success(request, "Bình chọn đã được xóa thành công.")
    return redirect('trang_chu')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from .models import BangHoi, BangTL



@login_required
def danh_sach_cau_hoi(request):
    # Lấy tất cả câu hỏi, sắp xếp theo thời gian tạo mới nhất
    cau_hoi_list = BangHoi.objects.all().order_by('-NgayTao')

    # Lấy người dùng hiện tại
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

    # Đếm số câu trả lời cho mỗi câu hỏi
    for cau_hoi in cau_hoi_list:
        cau_hoi.so_cau_tra_loi = BangTL.objects.filter(MaHoi=cau_hoi).count()

    context = {
        'cau_hoi_list': cau_hoi_list,
        'nguoi_dung': nguoi_dung,
    }

    return render(request, 'hoi_dap/danh_sach_cau_hoi.html', context)


@login_required
def chi_tiet_cau_hoi(request, cau_hoi_id):
    # Lấy chi tiết câu hỏi
    cau_hoi = get_object_or_404(BangHoi, id=cau_hoi_id)

    # Lấy danh sách câu trả lời
    cau_tra_loi_list = BangTL.objects.filter(MaHoi=cau_hoi).order_by('NgayTao')

    # Lấy người dùng hiện tại
    nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

    # Lấy các câu hỏi liên quan (5 câu hỏi mới nhất khác)
    cau_hoi_lien_quan = BangHoi.objects.exclude(id=cau_hoi_id).order_by('-NgayTao')[:5]

    context = {
        'cau_hoi': cau_hoi,
        'cau_tra_loi_list': cau_tra_loi_list,
        'nguoi_dung': nguoi_dung,
        'cau_hoi_lien_quan': cau_hoi_lien_quan,
    }

    return render(request, 'hoi_dap/chi_tiet_cau_hoi.html', context)


@login_required
def tao_cau_hoi(request):
    if request.method == 'POST':
        noi_dung = request.POST.get('NoiDung')

        # Lấy người dùng hiện tại
        nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

        # Tạo câu hỏi mới
        cau_hoi = BangHoi(
            NoiDung=noi_dung,
            NgayTao=timezone.now(),
            MaNguoiDung=nguoi_dung
        )
        cau_hoi.save()

        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi.id)

    return render(request, 'hoi_dap/tao_cau_hoi.html')


@login_required
def sua_cau_hoi(request, cau_hoi_id):
    # Lấy câu hỏi cần sửa
    cau_hoi = get_object_or_404(BangHoi, id=cau_hoi_id)

    # Kiểm tra quyền sửa (chỉ người tạo mới được sửa)
    if cau_hoi.MaNguoiDung.user != request.user:
        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi.id)

    if request.method == 'POST':
        noi_dung = request.POST.get('NoiDung')

        # Cập nhật câu hỏi
        cau_hoi.NoiDung = noi_dung
        cau_hoi.save()

        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi.id)

    context = {
        'cau_hoi': cau_hoi
    }

    return render(request, 'hoi_dap/sua_cau_hoi.html', context)


@login_required
def xoa_cau_hoi(request, cau_hoi_id):
    # Lấy câu hỏi cần xóa
    cau_hoi = get_object_or_404(BangHoi, id=cau_hoi_id)

    # Kiểm tra quyền xóa (chỉ người tạo mới được xóa)
    if cau_hoi.MaNguoiDung.user != request.user:
        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi.id)

    # Xóa câu hỏi
    cau_hoi.delete()

    return redirect('danh_sach_cau_hoi')


@login_required
def them_cau_tra_loi(request, cau_hoi_id):
    if request.method == 'POST':
        noi_dung = request.POST.get('NoiDung')

        # Lấy câu hỏi
        cau_hoi = get_object_or_404(BangHoi, id=cau_hoi_id)

        # Lấy người dùng hiện tại
        nguoi_dung = get_object_or_404(NguoiDung, user=request.user)

        # Tạo câu trả lời mới
        cau_tra_loi = BangTL(
            NoiDung=noi_dung,
            NgayTao=timezone.now(),
            MaHoi=cau_hoi,
            MaNguoiDung=nguoi_dung
        )
        cau_tra_loi.save()

    return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi_id)


@login_required
def sua_cau_tra_loi(request, cau_tra_loi_id):
    # Lấy câu trả lời cần sửa
    cau_tra_loi = get_object_or_404(BangTL, id=cau_tra_loi_id)

    # Kiểm tra quyền sửa (chỉ người tạo mới được sửa)
    if cau_tra_loi.MaNguoiDung.user != request.user:
        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_tra_loi.MaHoi.id)

    if request.method == 'POST':
        noi_dung = request.POST.get('NoiDung')

        # Cập nhật câu trả lời
        cau_tra_loi.NoiDung = noi_dung
        cau_tra_loi.save()

    return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_tra_loi.MaHoi.id)


@login_required
def xoa_cau_tra_loi(request, cau_tra_loi_id):
    # Lấy câu trả lời cần xóa
    cau_tra_loi = get_object_or_404(BangTL, id=cau_tra_loi_id)

    # Lưu lại id câu hỏi để redirect sau khi xóa
    cau_hoi_id = cau_tra_loi.MaHoi.id

    # Kiểm tra quyền xóa (chỉ người tạo mới được xóa)
    if cau_tra_loi.MaNguoiDung.user != request.user:
        return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi_id)

    # Xóa câu trả lời
    cau_tra_loi.delete()

    return redirect('chi_tiet_cau_hoi', cau_hoi_id=cau_hoi_id)
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from django.db.models import Q, Subquery, OuterRef
from django.contrib.auth.models import User
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_POST
from .models import CuocTroChuyen, TinNhanChiTiet


@login_required
def index(request):
    # Get all chats the user is a member of
    chats = CuocTroChuyen.objects.filter(ThanhVien=request.user)

    # Add last message and unread count to each chat
    for chat in chats:
        # Get last message
        last_message = TinNhanChiTiet.objects.filter(MaCuocTroChuyen=chat).order_by('-NgayTao').first()
        chat.last_message = last_message

        # Get unread count (in a real implementation, you would count unread messages)
        chat.unread_count = 0

    return render(request, 'chat/index.html', {
        'chats': chats
    })


@login_required
@csrf_exempt
@require_POST
def upload_file(request):
    """
    Nhận file từ FormData key='file', lưu vào thư mục MEDIA/uploads/files/,
    và trả về { id, name, url }.
    """
    upload = request.FILES.get('file')
    if not upload:
        return JsonResponse({'error': 'No file provided'}, status=400)

    # Tạo đường dẫn lưu: MEDIA_ROOT/uploads/files/<uuid>_<filename>
    filename = f"{uuid.uuid4().hex}_{upload.name}"
    save_path = os.path.join('uploads', 'files', filename)
    path = default_storage.save(save_path, ContentFile(upload.read()))

    url = default_storage.url(path)
    return JsonResponse({
        'id': path,         # dùng làm attachment_id
        'name': upload.name,
        'url': url
    })


@login_required
@csrf_exempt
@require_POST
def upload_image(request):
    """
    Nhận ảnh từ FormData key='image', lưu vào MEDIA/uploads/images/,
    và trả về { id, url }.
    """
    upload = request.FILES.get('image')
    if not upload:
        return JsonResponse({'error': 'No image provided'}, status=400)

    filename = f"{uuid.uuid4().hex}_{upload.name}"
    save_path = os.path.join('uploads', 'images', filename)
    path = default_storage.save(save_path, ContentFile(upload.read()))

    url = default_storage.url(path)
    return JsonResponse({
        'id': path,     # dùng làm image_id
        'url': url
    })
@login_required
def room_list(request):
    # Lấy tất cả phòng chat mà user là thành viên
    chats = CuocTroChuyen.objects.filter(ThanhVien=request.user)

    # Annotate last message và thời gian
    last_time_qs = TinNhanChiTiet.objects.filter(
        MaCuocTroChuyen=OuterRef('pk')
    ).order_by('-NgayTao').values('NgayTao')[:1]
    last_content_qs = TinNhanChiTiet.objects.filter(
        MaCuocTroChuyen=OuterRef('pk')
    ).order_by('-NgayTao').values('NoiDung')[:1]

    chats = chats.annotate(
        last_message_time=Subquery(last_time_qs),
        last_message_content=Subquery(last_content_qs)
    ).order_by('-last_message_time')

    room_data = []
    for chat in chats:
        # Đặt tên phòng: nếu private thì lấy tên người kia, ngược lại TenNhom
        if chat.LoaiRiengTu and chat.ThanhVien.count() == 2:
            other = chat.ThanhVien.exclude(id=request.user.id).first()
            room_name = other.username
            is_group = False
        else:
            room_name = chat.TenNhom or f"Nhóm {chat.id}"
            is_group = True

        room_data.append({
            'id': chat.id,
            'name': room_name,
            'is_group': is_group,
            'last_message': chat.last_message_content,
            'last_message_time': chat.last_message_time,
            'participants': list(chat.ThanhVien.values('id', 'username'))
        })

    return JsonResponse({'rooms': room_data})


@login_required
def room_messages(request, room_id):
    chat = get_object_or_404(CuocTroChuyen, id=room_id)
    if not chat.ThanhVien.filter(id=request.user.id).exists():
        return JsonResponse({'error': 'Không có quyền truy cập'}, status=403)

    msgs = TinNhanChiTiet.objects.filter(
        MaCuocTroChuyen=chat
    ).order_by('NgayTao')

    data = []
    for m in msgs:
        attachments = []
        if m.TepDinhKem:
            attachments.append({
                'type': 'file',
                'url': m.TepDinhKem.url,
                'name': m.TepDinhKem.name.split('/')[-1]
            })
        if m.HinhAnh:
            attachments.append({
                'type': 'image',
                'url': m.HinhAnh.url
            })
        data.append({
            'id': m.id,
            'content': m.NoiDung,
            'sender': {
                'id': m.NguoiDung.id,
                'username': m.NguoiDung.username,
            },
            'sender_avatar': getattr(m.NguoiDung, 'nguoidung').Avatar.url if hasattr(m.NguoiDung, 'nguoidung') and m.NguoiDung.nguoidung.Avatar else None,
            'timestamp': m.NgayTao.isoformat(),
            'attachments': attachments
        })

    return JsonResponse({'messages': data})


@login_required
@csrf_exempt
def create_private_room(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    other_id = data.get('user_id')
    if not other_id:
        return JsonResponse({'error': 'User ID is required'}, status=400)

    other = get_object_or_404(User, id=other_id)
    existing = CuocTroChuyen.objects.filter(
        LoaiRiengTu=True,
        ThanhVien=request.user
    ).filter(ThanhVien=other).first()
    if existing:
        return JsonResponse({'room_id': existing.id})

    chat = CuocTroChuyen.objects.create(LoaiRiengTu=True)
    chat.ThanhVien.add(request.user, other)
    return JsonResponse({'room_id': chat.id})


@login_required
@csrf_exempt
def create_group_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    name = request.POST.get('name')
    member_ids = request.POST.getlist('member_ids')
    avatar = request.FILES.get('avatar')

    if not name or not member_ids:
        return JsonResponse({'error': 'Name and members required'}, status=400)

    chat = CuocTroChuyen.objects.create(
        LoaiRiengTu=False,
        TenNhom=name,
        HinhAnh=avatar
    )
    chat.ThanhVien.add(request.user)
    for uid in member_ids:
        try:
            u = User.objects.get(id=uid)
            chat.ThanhVien.add(u)
        except User.DoesNotExist:
            continue

    return JsonResponse({'room_id': chat.id})


@login_required
def search_users(request):
    q = request.GET.get('q', '')
    if not q:
        return JsonResponse({'users': []})
    users = User.objects.filter(
        ~Q(id=request.user.id),
        Q(username__icontains=q)
    )[:10]
    return JsonResponse({
        'users': [{'id': u.id, 'username': u.username} for u in users]
    })


@login_required
def current_user(request):
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username
    })

from .forms import SearchForm


@login_required
def tim_kiem(request):
    form = SearchForm(request.GET or None)
    ket_qua = []
    if form.is_valid():
        q = form.cleaned_data['q']
        # Lọc bài viết theo nội dung chứa từ khóa
        ket_qua = BaiViet.objects.filter(NoiDung__icontains=q).order_by('-ThoiGianTao')
        # Thu thập tương tác và attachments cho mỗi bài
        # Map cảm xúc user hiện tại
        cx_map = {cx.MaBaiViet.id: cx.is_like for cx in LuotCamXuc.objects.filter(MaNguoiDung__user=request.user)}
        for post in ket_qua:
            post.anh_list = HinhAnh.objects.filter(MaBaiViet=post)
            post.file_list = TepDinhKem.objects.filter(MaBaiViet=post)
            post.so_thich = LuotCamXuc.objects.filter(MaBaiViet=post, is_like=True).count()
            post.so_khong_thich = LuotCamXuc.objects.filter(MaBaiViet=post, is_like=False).count()
            post.da_thich = cx_map.get(post.id)
            post.so_binh_luan = BinhLuan.objects.filter(MaBaiViet=post).count()
            post.binh_luan_list = BinhLuan.objects.filter(MaBaiViet=post).order_by('-NgayTao')
    return render(request, 'search.html', {
        'form': form,
        'ket_qua': ket_qua,
    })