import os
from django.utils.text import slugify
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

def path_foto_alumni(instance, filename):
    ext = filename.split('.')[-1]
    nama = slugify(instance.nama_lengkap)
    angkatan = instance.angkatan
    filename = f"{angkatan}_{nama}.{ext}"
    return os.path.join('foto_alumni', filename)

class Alumni(models.Model):
    nama_lengkap = models.CharField(max_length=100)
    angkatan = models.IntegerField()
    tanggal_lahir = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Kuliah', 'Kuliah'),
            ('Bekerja', 'Bekerja'),
            ('Menikah', 'Menikah'),
            ('Belum Bekerja', 'Belum Bekerja'),
        ],
        default='Belum Bekerja'
    )
    status_detail = models.CharField(max_length=100, blank=True, null=True)
    deskripsi_singkat = models.TextField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)  # ⬅️ Tambahan
    no_hp = models.CharField(max_length=20, blank=True, null=True)  # ⬅️ Tambahan
    foto = models.ImageField(upload_to=path_foto_alumni, blank=True, null=True)

    def __str__(self):
        return f"{self.nama_lengkap} - {self.angkatan}"

class RiwayatPendidikan(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='riwayat_pendidikan')
    jenjang = models.CharField(max_length=50)  # e.g. SD, SMP, SMA, S1, S2
    nama_institusi = models.CharField(max_length=100)
    tahun_masuk = models.PositiveIntegerField()
    tahun_lulus = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.jenjang} - {self.nama_institusi}"
    
@receiver(post_delete, sender=Alumni)
def hapus_foto_alumni(sender, instance, **kwargs):
    if instance.foto:
        instance.foto.delete(save=False)

from django.db.models.signals import pre_save

@receiver(pre_save, sender=Alumni)
def ganti_foto_lama(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        foto_lama = Alumni.objects.get(pk=instance.pk).foto
    except Alumni.DoesNotExist:
        return
    foto_baru = instance.foto
    if foto_lama and foto_lama != foto_baru:
        foto_lama.delete(save=False)

class KonfigurasiSitus(models.Model):
    form_tambah_alumni_aktif = models.BooleanField(default=False)

    def __str__(self):
        return "Konfigurasi Situs"

    class Meta:
        verbose_name = "Konfigurasi Situs"
        verbose_name_plural = "Konfigurasi Situs"

