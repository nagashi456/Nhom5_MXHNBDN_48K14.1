from django.shortcuts import render
def Binhluan(request):
    return render(request,"TaoBinhLuan/Taobinhluan.html")
def BinhChon(request):
    return render(request,"TaoBinhChon/TaoBinhChon.html")
def edit_profile(request):
    return render(request,"Edit_profile/edit_profile.html")
#1231234214124