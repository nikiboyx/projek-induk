from .models import Alumni

def daftar_angkatan(request):
    angkatan = Alumni.objects.values_list('angkatan', flat=True).distinct().order_by('-angkatan')
    return {'daftar_angkatan': angkatan}
