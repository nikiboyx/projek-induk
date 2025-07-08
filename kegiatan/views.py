from django.shortcuts import render, get_object_or_404, redirect
from .models import Kegiatan
from .forms import KegiatanForm, KomentarForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

# ✅ Home kegiatan
def kegiatan_home(request):
    kegiatan_list = Kegiatan.objects.order_by('-tanggal')
    return render(request, 'kegiatan/kegiatan_home.html', {
        'kegiatan_list': kegiatan_list
    })

# ✅ Detail kegiatan
def kegiatan_detail(request, slug):
    kegiatan = get_object_or_404(Kegiatan, slug=slug)
    komentar_list = kegiatan.komentar.all().order_by('-tanggal')

    if request.method == 'POST':
        form = KomentarForm(request.POST)
        if form.is_valid():
            komentar = form.save(commit=False)
            komentar.kegiatan = kegiatan
            komentar.save()
            return redirect('kegiatan_detail', slug=slug)
    else:
        form = KomentarForm()

    return render(request, 'kegiatan/kegiatan_detail.html', {
        'kegiatan': kegiatan,
        'form': form,
        'komentar_list': komentar_list
    })

# ✅ Cek apakah user admin
def hanya_admin(user):
    return user.is_authenticated and user.is_staff

# ✅ Kelola data kegiatan
@login_required
@user_passes_test(hanya_admin)
def kegiatan_manage(request):
    q = request.GET.get('q', '')
    kegiatan = Kegiatan.objects.all().order_by('-tanggal')
    if q:
        kegiatan = kegiatan.filter(
            Q(judul__icontains=q) |
            Q(isi__icontains=q)
        )
    return render(request, 'kegiatan/kegiatan_manage.html', {
        'kegiatan': kegiatan
    })

# ✅ Tambah kegiatan
@login_required
@user_passes_test(hanya_admin)
def kegiatan_tambah(request):
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('kegiatan_manage')
    else:
        form = KegiatanForm()
    return render(request, 'kegiatan/kegiatan_form.html', {
        'form': form,
        'judul': 'Tambah Kegiatan'
    })

# ✅ Edit kegiatan
@login_required
@user_passes_test(hanya_admin)
def kegiatan_edit(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    if request.method == 'POST':
        form = KegiatanForm(request.POST, request.FILES, instance=kegiatan)
        if form.is_valid():
            form.save()
            return redirect('kegiatan_manage')
    else:
        form = KegiatanForm(instance=kegiatan)
    return render(request, 'kegiatan/kegiatan_form.html', {
        'form': form,
        'judul': 'Edit Kegiatan'
    })

# ✅ Hapus kegiatan
@login_required
@user_passes_test(hanya_admin)
def kegiatan_hapus(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    if request.method == 'POST':
        kegiatan.delete()
        return redirect('kegiatan_manage')
    return render(request, 'kegiatan/kegiatan_konfirmasi_hapus.html', {
        'kegiatan': kegiatan
    })
