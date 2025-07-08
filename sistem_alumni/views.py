from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Alumni, KonfigurasiSitus
from .forms import AlumniForm

# Hanya bisa diakses oleh admin/staff
def hanya_admin(user):
    return user.is_authenticated and user.is_staff

# ✅ Kelola alumni (untuk admin)
@login_required
@user_passes_test(hanya_admin)
def manage_alumni(request):
    alumni = Alumni.objects.all().order_by('-angkatan')
    konfigurasi, created = KonfigurasiSitus.objects.get_or_create(id=1)
    q = request.GET.get('q', '')
    alumni = Alumni.objects.all()
    if q:
        alumni = alumni.filter(Q(nama_lengkap__icontains=q) | Q(angkatan__icontains=q))
    return render(request, 'sistem_alumni/manage_alumni.html', {
        'alumni': alumni,
        'konfigurasi': konfigurasi
    })

# ✅ Tambah alumni
@login_required
@user_passes_test(hanya_admin)
def alumni_tambah(request):
    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Data alumni berhasil ditambahkan.")
            return redirect('manage_alumni')
        else:
            messages.error(request, "Gagal menambahkan data. Periksa kembali input Anda.")
    else:
        form = AlumniForm()
    return render(request, 'sistem_alumni/alumni_form.html', {
        'form': form,
        'judul': 'Tambah Alumni'
    })

def alumni_tambah_umum(request):
    konfigurasi = KonfigurasiSitus.objects.first()
    if not konfigurasi or not konfigurasi.form_tambah_alumni_aktif:
        messages.warning(request, "Formulir tambah alumni sedang tidak tersedia.")
        return redirect('sas_home')

    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Data alumni berhasil dikirim.")
            return redirect('sas_home')
        else:
            messages.error(request, "Gagal mengirim data. Silakan periksa kembali.")
    else:
        form = AlumniForm()

    return render(request, 'sistem_alumni/alumni_form.html', {
        'form': form,
        'judul': 'Form Tambah Alumni (Umum)'
    })

# ✅ Edit alumni
@login_required
@user_passes_test(hanya_admin)
def alumni_edit(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, "Data alumni berhasil diperbarui.")
            return redirect('manage_alumni')
        else:
            messages.error(request, "Gagal menyimpan perubahan.")
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'sistem_alumni/alumni_form.html', {
        'form': form,
        'judul': 'Edit Alumni'
    })

# ✅ Hapus alumni
@login_required
@user_passes_test(hanya_admin)
def alumni_hapus(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        alumni.delete()
        messages.success(request, f"Data alumni '{alumni.nama_lengkap}' berhasil dihapus.")
        return redirect('manage_alumni')
    return render(request, 'sistem_alumni/alumni_konfirmasi_hapus.html', {
        'alumni': alumni
    })

# ✅ Hapus alumni batch
@login_required
@user_passes_test(hanya_admin)
def alumni_batch_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_ids')
        if ids:
            Alumni.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} alumni berhasil dihapus.")
        else:
            messages.warning(request, "Tidak ada data yang dipilih.")
    return redirect('manage_alumni')

# ✅ Halaman Beranda
def sas_home(request):
    konfigurasi = KonfigurasiSitus.objects.first()
    alumni = Alumni.objects.order_by('-angkatan')[:4]
    return render(request, 'sistem_alumni/home.html', {
        'alumni': alumni,
        'konfigurasi': konfigurasi
    })

# ✅ Daftar semua alumni
def alumni_semua(request):
    alumni = Alumni.objects.all().order_by('-angkatan')
    konfigurasi, created = KonfigurasiSitus.objects.get_or_create(id=1)
    return render(request, 'sistem_alumni/alumni_semua.html', {
        'alumni': alumni,
        'konfigurasi': konfigurasi
    })

# ✅ Alumni berdasarkan angkatan
def alumni_angkatan(request, tahun):
    alumni = Alumni.objects.filter(angkatan=tahun)
    konfigurasi, created = KonfigurasiSitus.objects.get_or_create(id=1)
    return render(request, 'sistem_alumni/alumni_angkatan.html', {
        'angkatan': tahun,
        'alumni': alumni,
        'konfigurasi': konfigurasi
    })

# ✅ Pencarian alumni
def cari_alumni(request):
    q = request.GET.get('q', '')
    hasil = Alumni.objects.none()
    konfigurasi, created = KonfigurasiSitus.objects.get_or_create(id=1)
    if q:
        hasil = Alumni.objects.filter(
            Q(nama_lengkap__icontains=q) |
            Q(angkatan__icontains=q)
        )
    return render(request, 'sistem_alumni/cari_alumni.html', {
        'hasil': hasil, 'konfigurasi': konfigurasi
    })

@login_required
@user_passes_test(hanya_admin)
def admin_konfigurasi(request):
    konfigurasi, created = KonfigurasiSitus.objects.get_or_create(id=1)

    if request.method == 'POST':
        status = request.POST.get('form_tambah_alumni_aktif') == 'on'
        konfigurasi.form_tambah_alumni_aktif = status
        konfigurasi.save()
        messages.success(request, "Pengaturan berhasil diperbarui.")
        return redirect('admin_konfigurasi')

    return render(request, 'sistem_alumni/admin_konfigurasi.html', {
        'konfigurasi': konfigurasi
    })