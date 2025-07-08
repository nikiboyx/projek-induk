from django.db import models
from django.utils import timezone
import os
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

def kegiatan_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    slug = slugify(instance.judul)[:50]
    filename = f"{slug}-{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('kegiatan', filename)

class Kegiatan(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    isi = models.TextField()
    gambar = models.ImageField(upload_to=kegiatan_upload_path, blank=True, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

class Komentar(models.Model):
    kegiatan = models.ForeignKey('Kegiatan', on_delete=models.CASCADE, related_name='komentar')
    nama = models.CharField(max_length=100)
    isi = models.TextField()
    tanggal = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nama} - {self.kegiatan.judul}"

# logic
@receiver(pre_save, sender=Kegiatan)
def hapus_file_lama_kegiatan(sender, instance, **kwargs):
    if not instance.pk:
        return  # skip create
    try:
        kegiatan_lama = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    if kegiatan_lama.gambar and kegiatan_lama.gambar != instance.gambar:
        if os.path.isfile(kegiatan_lama.gambar.path):
            os.remove(kegiatan_lama.gambar.path)

@receiver(post_delete, sender=Kegiatan)
def hapus_file_saat_dihapus(sender, instance, **kwargs):
    if instance.gambar and os.path.isfile(instance.gambar.path):
        os.remove(instance.gambar.path)


