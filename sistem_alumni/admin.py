from django.contrib import admin
from .models import Alumni, RiwayatPendidikan
from .models import KonfigurasiSitus

class RiwayatPendidikanInline(admin.TabularInline):
    model = RiwayatPendidikan
    extra = 1

class AlumniAdmin(admin.ModelAdmin):
    list_display = ('nama_lengkap', 'angkatan', 'status', 'status_detail')

@admin.register(KonfigurasiSitus)
class KonfigurasiSitusAdmin(admin.ModelAdmin):
    list_display = ['form_tambah_alumni_aktif']

