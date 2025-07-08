# kegiatan/forms.py
from django import forms
from .models import Kegiatan, Komentar

class KegiatanForm(forms.ModelForm):
    isi = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'border border-gray-300 px-3 py-2 rounded w-full',
            'placeholder': 'Isi konten kegiatan...'
        }),
        label='Isi Konten'
    )

    class Meta:
        model = Kegiatan
        fields = ['judul', 'isi', 'gambar']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'border border-gray-300 px-3 py-2 rounded w-full',
                'placeholder': 'Judul kegiatan...'
            }),
            'gambar': forms.ClearableFileInput(attrs={
                'class': 'border border-gray-300 px-3 py-2 rounded w-full'
            })
        }

class KomentarForm(forms.ModelForm):
    class Meta:
        model = Komentar
        fields = ['nama', 'isi']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'border px-3 py-2 rounded w-full'}),
            'isi': forms.Textarea(attrs={'class': 'border px-3 py-2 rounded w-full', 'rows': 3}),
        }
