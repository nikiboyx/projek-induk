from django.urls import path
from . import views

urlpatterns = [
    # Publik
    path('', views.kegiatan_home, name='kegiatan_home'),
    path('<slug:slug>/', views.kegiatan_detail, name='kegiatan_detail'),

    # Admin CRUD (pakai prefix admin/)
    path('admin/manage/', views.kegiatan_manage, name='kegiatan_manage'),
    path('admin/tambah/', views.kegiatan_tambah, name='kegiatan_tambah'),
    path('admin/<int:pk>/edit/', views.kegiatan_edit, name='kegiatan_edit'),
    path('admin/<int:pk>/hapus/', views.kegiatan_hapus, name='kegiatan_hapus'),
]
