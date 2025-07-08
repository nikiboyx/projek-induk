from django import forms
from .models import Alumni

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = [
            'nama_lengkap', 'angkatan', 'tanggal_lahir',
            'status', 'status_detail', 'alamat', 'no_hp',
            'deskripsi_singkat', 'foto'
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'angkatan': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'status': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'status_detail': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'no_hp': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
            'alamat': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 3}),
            'deskripsi_singkat': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
        }
