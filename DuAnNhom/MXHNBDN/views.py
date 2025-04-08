from django.shortcuts import render
def Binhluan(request):
    return render(request,"TaoBinhLuan/Taobinhluan.html")
def edit_profile(request):
    return render(request,"Edit_profile/edit_profile.html")

def index(request):
    return render(request,"base.html")
def detail_profile(request):
    return render(request,"Edit_profile/profile_details.html")
