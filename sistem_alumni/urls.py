from django.urls import path
from . import views

urlpatterns = [
    path('', views.sas_home, name='sas_home'),
    path('semua/', views.alumni_semua, name='alumni_semua'),
    path('angkatan/<int:tahun>/', views.alumni_angkatan, name='alumni_angkatan'),
    path('cari/', views.cari_alumni, name='cari_alumni'),

    path('admin/manage/', views.manage_alumni, name='manage_alumni'),
    path('admin/manage/create/', views.alumni_tambah, name='alumni_tambah'),
    path('admin/manage/<int:pk>/edit/', views.alumni_edit, name='alumni_edit'),
    path('admin/manage/<int:pk>/delete/', views.alumni_hapus, name='alumni_hapus'),
    path('alumni/batch-delete/', views.alumni_batch_delete, name='alumni_batch_delete'),

    path('alumni/tambah/', views.alumni_tambah_umum, name='alumni_tambah_umum'),
    path('admin/konfigurasi/', views.admin_konfigurasi, name='admin_konfigurasi'),
]
