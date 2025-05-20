from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, UsernameChangeForm, CustomPasswordChangeForm, LuaChonBinhChonFormSet
from .models import NguoiDung, BaiViet, BinhChonNhom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NguoiDung, BinhChon
from .forms import BinhChonForm
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm, NguoiDungForm

def DangNhap(request):
    return render(request,"DangNhap.html")

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


def ProfileDetail(request):
    return render(request,"Edit_profile/profile_details.html")


@login_required
def Trangchu(request):
    return render(request,"Trangchu.html")
def Quenpass(request):
    return render(request,"Quenpass.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import (
    CuocTroChuyen, NguoiDung, TinNhanChiTiet,
    ThanhVienCuocTroChuyen, PhongBan
)
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def index(request):
    """
    Main chat page showing all conversations
    """
    user = request.user
    nguoi_dung = NguoiDung.objects.get(user=user)

    # Get all conversations where the user is a member
    conversations = CuocTroChuyen.objects.filter(
        thanhviencuoctrochuyen__MaNguoiDung=nguoi_dung
    ).distinct()

    # Get the last message for each conversation
    conversations_with_last_message = []
    for conv in conversations:
        last_message = TinNhanChiTiet.objects.filter(
            MaCuocTroChuyen=conv
        ).order_by('-NgayTao').first()

        conversations_with_last_message.append({
            'conversation': conv,
            'last_message': last_message
        })

    return render(request, 'chat/index.html', {
        'conversations': conversations_with_last_message,
        'current_user': nguoi_dung
    })


@login_required
def conversation(request, conversation_id):
    """
    View a specific conversation
    """
    user = request.user
    nguoi_dung = NguoiDung.objects.get(user=user)

    # Get the conversation
    conversation = get_object_or_404(CuocTroChuyen, id=conversation_id)

    # Check if user is a member of this conversation
    is_member = ThanhVienCuocTroChuyen.objects.filter(
        MaCuocTroChuyen=conversation,
        MaNguoiDung=nguoi_dung
    ).exists()

    if not is_member:
        return redirect('chat:index')

    # Get all messages in this conversation
    messages = TinNhanChiTiet.objects.filter(
        MaCuocTroChuyen=conversation
    ).order_by('NgayTao')

    # Get all members of this conversation
    members = ThanhVienCuocTroChuyen.objects.filter(
        MaCuocTroChuyen=conversation
    )

    # Get all conversations where the user is a member (for sidebar)
    all_conversations = CuocTroChuyen.objects.filter(
        thanhviencuoctrochuyen__MaNguoiDung=nguoi_dung
    ).distinct()

    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'members': members,
        'all_conversations': all_conversations,
        'current_user': nguoi_dung
    })


@login_required
def create_private_chat(request):
    """
    Create a private chat between two users
    """
    if request.method == 'POST':
        user = request.user
        nguoi_dung = NguoiDung.objects.get(user=user)
        other_user_id = request.POST.get('user_id')
        other_nguoi_dung = get_object_or_404(NguoiDung, id=other_user_id)

        # Check if a private conversation already exists between these users
        existing_conversation = CuocTroChuyen.objects.filter(
            Loai=False,  # Private chat
            thanhviencuoctrochuyen__MaNguoiDung=nguoi_dung
        ).filter(
            thanhviencuoctrochuyen__MaNguoiDung=other_nguoi_dung
        ).distinct()

        if existing_conversation.exists() and existing_conversation.count() == 1:
            # If exists, redirect to that conversation
            return redirect('chat:conversation', conversation_id=existing_conversation.first().id)

        # Create a new private conversation
        conversation = CuocTroChuyen.objects.create(
            Loai=False,  # Private chat
            TenNhom=None,
            HinhAnh=None
        )

        # Add both users as members
        ThanhVienCuocTroChuyen.objects.create(
            MaCuocTroChuyen=conversation,
            MaNguoiDung=nguoi_dung,
            NgayGiaNhap=timezone.now()
        )

        ThanhVienCuocTroChuyen.objects.create(
            MaCuocTroChuyen=conversation,
            MaNguoiDung=other_nguoi_dung,
            NgayGiaNhap=timezone.now()
        )

        return redirect('chat:conversation', conversation_id=conversation.id)

    # If GET request, show form to select a user
    user = request.user
    nguoi_dung = NguoiDung.objects.get(user=user)

    # Get all users except current user
    other_users = NguoiDung.objects.exclude(id=nguoi_dung.id)

    return render(request, 'chat/create_private_chat.html', {
        'users': other_users,
        'current_user': nguoi_dung
    })


@login_required
def create_group_chat(request):
    """
    Create a group chat
    """
    if request.method == 'POST':
        user = request.user
        nguoi_dung = NguoiDung.objects.get(user=user)
        group_name = request.POST.get('group_name')
        member_ids = request.POST.getlist('member_ids')

        # Create a new group conversation
        conversation = CuocTroChuyen.objects.create(
            Loai=True,  # Group chat
            TenNhom=group_name,
            HinhAnh=request.FILES.get('group_image', None)
        )

        # Add current user as a member
        ThanhVienCuocTroChuyen.objects.create(
            MaCuocTroChuyen=conversation,
            MaNguoiDung=nguoi_dung,
            NgayGiaNhap=timezone.now()
        )

        # Add selected users as members
        for member_id in member_ids:
            member = NguoiDung.objects.get(id=member_id)
            if member.id != nguoi_dung.id:  # Don't add current user twice
                ThanhVienCuocTroChuyen.objects.create(
                    MaCuocTroChuyen=conversation,
                    MaNguoiDung=member,
                    NgayGiaNhap=timezone.now()
                )

        return redirect('chat:conversation', conversation_id=conversation.id)

    # If GET request, show form to create a group
    user = request.user
    nguoi_dung = NguoiDung.objects.get(user=user)

    # Get all users except current user
    other_users = NguoiDung.objects.exclude(id=nguoi_dung.id)

    return render(request, 'chat/create_group_chat.html', {
        'users': other_users,
        'current_user': nguoi_dung
    })


@login_required
def search_users(request):
    """
    API endpoint to search for users
    """
    query = request.GET.get('q', '')
    user = request.user
    nguoi_dung = NguoiDung.objects.get(user=user)

    users = NguoiDung.objects.filter(
        Q(HoTen__icontains=query) |
        Q(Email__icontains=query)
    ).exclude(id=nguoi_dung.id)[:10]

    results = []
    for user in users:
        results.append({
            'id': user.id,
            'name': user.HoTen,
            'email': user.Email,
            'avatar': user.Avatar.url if user.Avatar else None,
            'department': user.MaPhong.TenPhong
        })

    return JsonResponse({'results': results})


@csrf_exempt
@login_required
def upload_attachment(request):
    """
    API endpoint to upload file attachments
    """
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        # Process the file (you might want to validate file type, size, etc.)

        # For simplicity, we'll just return the URL
        # In a real app, you'd save this to your storage and return the URL
        return JsonResponse({
            'success': True,
            'file_url': '/media/tepdinhkem/' + file.name,
            'file_size': file.size
        })

    return JsonResponse({'success': False, 'error': 'No file provided'})



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



@login_required
def edit_profile(request):
    # Lấy thông tin người dùng hiện tại
    user = request.user
    try:
        nguoi_dung = NguoiDung.objects.get(user=user)
    except NguoiDung.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin người dùng")
        return redirect('trang_chu')

    # Đếm số bài viết
    post_count = BaiViet.objects.filter(MaNguoiDung=nguoi_dung).count()

    # Xử lý form
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
                update_session_auth_hash(request, user)  # Giữ người dùng đăng nhập
                messages.success(request, "Cập nhật mật khẩu thành công!")
                return redirect('edit_profile')
    else:
        profile_form = UserProfileForm(instance=nguoi_dung)
        username_form = UsernameChangeForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    context = {
        'profile_form': profile_form,
        'username_form': username_form,
        'password_form': password_form,
        'nguoi_dung': nguoi_dung,
        'post_count': post_count,
        'hide_sidebar': False,  # Hiển thị sidebar
        'show_search': False,  # Không hiển thị thanh tìm kiếm
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
    return render(request, 'TaoBinhChon\TaoBinhChon.html', context)


@login_required
def danh_sach_binh_chon(request):
    nguoi_dung = NguoiDung.objects.get(user=request.user)
    binh_chons = BinhChon.objects.all().order_by('-ThoiGianKetThucBC')

    context = {
        'binh_chons': binh_chons,
        'nguoidung': nguoi_dung,  # Thêm thông tin người dùng cho template
    }
    return render(request, 'TaoBinhChon\danh_sach_binh_chon.html', context)

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