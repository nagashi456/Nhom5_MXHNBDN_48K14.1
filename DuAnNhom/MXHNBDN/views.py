from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
def DangNhap(request):
    return render(request,"DangNhap.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import BaiViet, HinhAnh, TepDinhKem
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def danh_sach_bai_viet(request):
    baiviet_list = BaiViet.objects.filter(MaNguoiDung=request.user).order_by('-ThoiGianTao')
    return render(request, 'baiviet/danh_sach_bai_viet.html', {'baiviet_list': baiviet_list})

@login_required
def tao_bai_viet(request):
    if request.method == 'POST':
        form = BaiVietForm(request.POST)
        if form.is_valid():
            baiviet = form.save(commit=False)
            baiviet.MaNguoiDung = request.user
            baiviet.ThoiGianTao = timezone.now()
            baiviet.save()

            for f in request.FILES.getlist('Anh'):
                HinhAnh.objects.create(Anh=f, ImgSize=f.size, MaBaiViet=baiviet)

            for f in request.FILES.getlist('Tep'):
                TepDinhKem.objects.create(Tep=f, FileSize=f.size, MaBaiViet=baiviet)

            return redirect('danh_sach_bai_viet')
    else:
        form = BaiVietForm()
    return render(request, 'baiviet/tao_bai_viet.html', {'form': form})

@login_required
def sua_bai_viet(request, pk):
    baiviet = get_object_or_404(BaiViet, pk=pk, MaNguoiDung=request.user)
    if request.method == 'POST':
        form = BaiVietForm(request.POST, instance=baiviet)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_bai_viet')
    else:
        form = BaiVietForm(instance=baiviet)
    return render(request, 'baiviet/sua_bai_viet.html', {'form': form})

@login_required
def xoa_bai_viet(request, pk):
    baiviet = get_object_or_404(BaiViet, pk=pk, MaNguoiDung=request.user)
    if request.method == 'POST':
        baiviet.delete()
        return redirect('danh_sach_bai_viet')
    return render(request, 'baiviet/xoa_bai_viet.html', {'baiviet': baiviet})


# def tao_bai_viet(request):
#     # Get the admin user from your custom NguoiDung model
#     try:
#         # Try to get the first admin user from NguoiDung model
#         admin_user = NguoiDung.objects.filter(is_superuser=True).first()
#         if not admin_user:
#             # If no admin exists, try to get any user
#             admin_user = NguoiDung.objects.first()
#             if not admin_user:
#                 # If no users exist, show an error message
#                 messages.error(request,
#                                'Không tìm thấy người dùng nào trong hệ thống. Vui lòng tạo một tài khoản admin trước.')
#                 return redirect('trang_chu')
#     except Exception as e:
#         messages.error(request, f'Lỗi khi tìm người dùng: {str(e)}')
#         return redirect('trang_chu')
#
#     if request.method == 'POST':
#         form = BaiVietForm(request.POST, request.FILES)
#         if form.is_valid():
#             bai_viet = form.save(commit=False)
#             # Use the admin user from NguoiDung model
#             bai_viet.nguoi_dung = admin_user
#             bai_viet.save()
#             messages.success(request, 'Bài viết đã được đăng thành công!')
#             return redirect('trang_chu')
#     else:
#         form = BaiVietForm()
#
#     # Pass the admin username to the template for display
#     return render(request, 'TaoBaiViet.html', {
#         'form': form,
#         'admin_username': admin_user.username
#     })
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
