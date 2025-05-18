from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
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
