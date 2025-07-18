# Generated by Django 5.2.4 on 2025-07-07 16:24

import sistem_alumni.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistem_alumni', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumni',
            old_name='alamat',
            new_name='deskripsi_singkat',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='email',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='no_telepon',
        ),
        migrations.RemoveField(
            model_name='alumni',
            name='status_saat_ini',
        ),
        migrations.AddField(
            model_name='alumni',
            name='status',
            field=models.CharField(choices=[('Kuliah', 'Kuliah'), ('Bekerja', 'Bekerja'), ('Menikah', 'Menikah'), ('Belum Bekerja', 'Belum Bekerja')], default='Belum Bekerja', max_length=50),
        ),
        migrations.AddField(
            model_name='alumni',
            name='status_detail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='angkatan',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=sistem_alumni.models.path_foto_alumni),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True),
        ),
    ]
