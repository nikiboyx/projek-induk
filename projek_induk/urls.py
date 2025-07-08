from django.contrib import admin
from django.urls import path, include
from . import views
from .views import halaman_utama  # Import view yang baru kita buat
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', halaman_utama, name='halaman_utama'),
    path('admin/', admin.site.urls),
    path('sas/', include('sistem_alumni.urls')),
    path('kegiatan/', include('kegiatan.urls')),

    path('akun/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)